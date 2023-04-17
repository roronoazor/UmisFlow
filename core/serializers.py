from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from authentication.serializers import UserSerializer


class ProfileSerializer(ModelSerializer):
    
    user_data = SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
    
    def get_user_data(self, instance):
        if instance.user:
            serializer = UserSerializer(instance.user)
            return serializer.data
        return dict()

class MealTypeSerializer(ModelSerializer):

    class Meta:
        model = MealType
        fields = '__all__'

class UserMealTypeSerializer(ModelSerializer):

    meal_type_data = SerializerMethodField()

    class Meta:
        model = UsersMealType
        fields = '__all__'

    def get_meal_type_data(self, obj):
        return MealTypeSerializer(obj.meal_type).data

class ResidenceSerializer(ModelSerializer):

    class Meta:
        model = Residence
        fields = '__all__'

class CoursesSerializer(ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'

class UserResidenceSerializer(ModelSerializer):

    residence_data = SerializerMethodField()

    class Meta:
        model = UsersResidence
        fields = '__all__'

    def get_residence_data(self, obj):
        return ResidenceSerializer(obj.residence).data

class WorshipCenterSerializer(ModelSerializer):

    class Meta:
        model = WorshipCenter
        fields = '__all__'

class UsersWorshipCenterSerializer(ModelSerializer):

    worship_center_data = SerializerMethodField()

    class Meta:
        model = UsersWorshipCenter
        fields = '__all__'

    def get_worship_center_data(self, obj):
        return WorshipCenterSerializer(obj.worship_center).data

class UserCoursesSerializer(ModelSerializer):

    course_data = SerializerMethodField()
    semester_data = SerializerMethodField()

    class Meta:
        model = UsersCourses
        fields = '__all__'

    def get_course_data(self, obj):
        return CoursesSerializer(obj.course).data

    def get_semester_data(self, obj):
        return SemesterSerializer(obj.semester).data

class SemesterSerializer(ModelSerializer):

    class Meta:
        model = Semester
        fields = '__all__'

class UserSemesterSerializer(ModelSerializer):

    semester = SemesterSerializer()

    class Meta:
        model = UserSemester
        fields = '__all__'