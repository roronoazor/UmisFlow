from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    matric_no = models.CharField(max_length=50, blank=True, null=True)
    programme = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    entry_level = models.CharField(max_length=50, blank=True, null=True)
    study_level = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    denomination = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    on_probration = models.BooleanField(blank=True, null=True)
    off_campus = models.BooleanField(blank=True, null=True)
    school_details = models.TextField(blank=True, null=True)
    department_details = models.TextField(blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    etranzact_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    sub = models.CharField(max_length=50, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s profile" % (self.user.first_name, self.user.last_name)


class WorshipCenter(models.Model):
    worship_center = models.CharField(max_length=100, blank=True, null=True)
    location_on_campus = models.CharField(max_length=100, blank=True, null=True)
    pastor_in_charge = models.CharField(max_length=100, blank=True, null=True)
    space_left = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "%s" % (self.worship_center)
    

class Residence(models.Model):
    residence_id = models.CharField(max_length=50, blank=True, null=True)
    residence_name = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    available_space = models.IntegerField(blank=True, null=True)
    minimum_level = models.CharField(max_length=50, blank=True, null=True)
    maximum_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.residence_name,)


class MealType(models.Model):
    selection = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s" % (self.selection,)


class Courses(models.Model):
    course_id = models.CharField(max_length=50, blank=True, null=True)
    course_title = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    credit = models.FloatField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    gp = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "%s" % (self.course_title, )


class Semester(models.Model):
    
    semester = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.semester,)


class UserSemester(models.Model):

    study_level = models.CharField(max_length=50, blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    credit_hours = models.FloatField(blank=True, null=True)
    credit_gpa = models.FloatField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s - %s %s" % (self.semester.semester, self.user.first_name, self.user.last_name)
    

class UsersCourses(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    space_left = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class UsersResidence(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, blank=True, null=True)
    space_left = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.user.first_name, self.user.last_name, self.residence.residence_name)
    

class UsersMealType(models.Model):
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, blank=True, null=True)
    space_left = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.user.first_name, self.user.last_name, self.meal_type.selection)
    

class UsersWorshipCenter(models.Model):
    worship_center = models.ForeignKey(WorshipCenter, on_delete=models.CASCADE, blank=True, null=True)
    space_left = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.user.first_name, self.user.last_name, self.worship_center.worship_center)
    