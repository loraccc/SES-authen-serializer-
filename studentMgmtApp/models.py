from django.db import models
from datetime import datetime

# Create your models here.
class AppUser(models.Model):
    full_name = models.CharField(max_length=200)
    contact = models.CharField(unique=True, max_length=200)
    email = models.EmailField(unique=True)
    usertype = models.CharField(max_length=200)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "app_users"

class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.title
        
    class Meta:
        db_table = "app_courses"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100)
    academic_level = models.CharField(max_length=200)
    academic_status = models.CharField(max_length=100)
    academic_org = models.CharField(max_length=200)
    academic_score = models.CharField(max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    intake = models.CharField(max_length=200, null=True, blank=True)
    shift = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=200)
    visited_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "app_students"



