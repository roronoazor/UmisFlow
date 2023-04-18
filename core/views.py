from django.shortcuts import render
from rest_framework import generics, status, response
from rest_framework.permissions import IsAuthenticated
from  authentication.authentication import BearerTokenAuthentication
from django.db.models import Count
from .serializers import *
from datetime import datetime, time
from rest_framework.views import APIView
from .models import *

class UserDetailsView(APIView):

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()

        if not profile:
            profile = Profile()

        profile_serializer = ProfileSerializer(profile)

        data = profile_serializer.data
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        request.data["user"] = request.user.id

        profile = Profile.objects.filter(user=request.user).first()

        if profile:
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if request.data.get('email'):
                request.user.email = request.data.get('email')
                request.user.save()
        else:
            profile = Profile()
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            instance = serializer.save()
            return response.Response({"message": "success", "detail": serializer.data}, status=status.HTTP_200_OK)
        return response.Response({"message": "failed", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SelectMealTypeView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        meal_types = MealType.objects.all()
        meal_type_serializer = MealTypeSerializer(meal_types, many=True)

        user_meal_type = UsersMealType.objects.all()
        user_meal_type_serializer = UserMealTypeSerializer(user_meal_type, many=True)

        data = {
            "meal_types": meal_type_serializer.data,
            "user_meal_types": user_meal_type_serializer.data
        }
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_meal_types = UsersMealType.objects.filter(user=request.user).delete()

        ids = request.data.get('ids')
        meal_types = MealType.objects.filter(id__in=ids)
        for meal_type in meal_types:
            UsersMealType.objects.create(
                meal_type=meal_type,
                user=request.user
            )
        return response.Response({"message": "success"}, status=status.HTTP_200_OK)


class SelectResidenceView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        residences = Residence.objects.all()
        residence_serializer = ResidenceSerializer(residences, many=True)

        user_residences = UsersResidence.objects.all()
        user_residences_serializer = UserResidenceSerializer(user_residences, many=True)

        data = {
            "residences": residence_serializer.data,
            "user_residences": user_residences_serializer.data
        }
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        UsersResidence.objects.filter(user=request.user).delete()

        residences  = Residence.objects.filter(id__in=request.data.get("ids"))

        for residence in residences:
            UsersResidence.objects.create(
                residence=residence,
                user=request.user
            )

            available = residence.available_space or 0
            residence.available_space = available - 1
            residence.save()
        return response.Response({"message": "success"}, status=status.HTTP_200_OK)


class SelectWorshipCenterView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        worships = WorshipCenter.objects.all()
        worship_serializer = WorshipCenterSerializer(worships, many=True)

        user_worship_centers = UsersWorshipCenter.objects.all()
        user_worship_serializer = UsersWorshipCenterSerializer(user_worship_centers, many=True)

        data = {
            "worships": worship_serializer.data,
            "user_worships": user_worship_serializer.data
        }
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        UsersWorshipCenter.objects.filter(user=request.user).delete()

        worships = WorshipCenter.objects.filter(id__in=request.data.get("ids"))

        for worship in worships:
            UsersWorshipCenter.objects.create(
                worship_center=worship,
                user=request.user
            )

            left = worship.space_left or 0
            worship.space_left = left - 1
            worship.save()
        return response.Response({"message": "success"}, status=status.HTTP_200_OK)


class SelectUserCoursesView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if not self.kwargs.get("id") or self.kwargs.get("id") == 9999:
            # get the latest semester for the user
            latest_semester = UserSemester.objects.filter(user=request.user).order_by('-id').first()
            latest_semester_id = latest_semester.id or 9999
        else:
            latest_semester_id = self.kwargs.get("id")

        courses = UsersCourses.objects.filter(
            user=request.user,
            semester=self.kwargs.get("id", latest_semester_id)
            )
        courses_serializer = UserCoursesSerializer(courses, many=True)

        data = {
            "courses": courses_serializer.data,
        }
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        pass


class SemesterView(APIView):

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        semesters = UserSemester.objects.filter(user=request.user)
        semesters_serializer = UserSemesterSerializer(semesters, many=True)

        data = {
            "semester": semesters_serializer.data
        }
        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)


class SubmitRegistrationView(APIView):

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict()

        profile = Profile.objects.filter(user=request.user).first()

        if not profile:
           profile = Profile()

        user_meal_type = UsersMealType.objects.filter(
            user=request.user
        ).first()

        user_residence = UsersResidence.objects.filter(
            user=request.user
        ).first()
           
        data["semester"] = "2022/2023"
        data["matric_no"] = profile.matric_no
        data["student_name"] = "%s %s" % (request.user.first_name, request.user.last_name)
        data["school"] = profile.school_details
        data["study_level"] = profile.study_level
        data["selected_meal"] = user_meal_type.meal_type.selection if user_meal_type else ""
        data["selected_resident"] = user_residence.residence.residence_name if user_residence else ""
        data["off_campus"] = profile.off_campus
        data["financial_approval"] = "Yes"
        data["completed_registration"] = profile.completed_registration
        data["selected_credit_hours"] = 25

        return response.Response({"message": "success", "detail": data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        profile = Profile.objects.filter(user=request.user).first()
        profile.completed_registration = True
        profile.save()
        
        return response.Response({"message": "success"}, status=status.HTTP_200_OK)

