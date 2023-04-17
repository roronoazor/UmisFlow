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
        pass


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
        pass


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
        pass


class SelectUserCoursesView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        courses = UsersCourses.objects.filter(
            user=request.user,
            semester=self.kwargs.get("id")
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
