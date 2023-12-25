from rest_framework import serializers
from .models import Student, Course, AppUser

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ("visited_at",)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("title", "code")

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("full_name", "email", "password", "usertype", "contact")

    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")