from django.contrib import admin
from django.apps import apps
from .models import *

admin.site.register(Profile)
admin.site.register(WorshipCenter)
admin.site.register(Residence)
admin.site.register(MealType)
admin.site.register(Courses)
admin.site.register(Semester)
admin.site.register(UsersCourses)
admin.site.register(UsersResidence)
admin.site.register(UsersMealType)
admin.site.register(UsersWorshipCenter)
admin.site.register(UserSemester)