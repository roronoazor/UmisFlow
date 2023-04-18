from django.urls import path
from .views import *

urlpatterns = [
    path("user_details/", UserDetailsView.as_view(), name="user_details"),
    path("user_meal_types/", SelectMealTypeView.as_view(), name="user_meal_types"),
    path("user_residences/", SelectResidenceView.as_view(), name="user_residences"),
    path("user_worship_centers/", SelectWorshipCenterView.as_view(), name="user_worship_centers"),
    path("user_semesters/", SemesterView.as_view(), name="user_semesters"),
    path("user_semester_courses/<int:id>/", SelectUserCoursesView.as_view(), name="user_semesters_courses"),
    path("submit_registration/", SubmitRegistrationView.as_view(), name="submit_registration"),
]
