from django import forms
from .models import AppUser, Student, Course

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        # fields='__all__'
        fields = ("full_name", "email", "password", "usertype", "contact")
        model = AppUser

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ("email", "password")
        # fields = "__all__" - incase of all fields
        model = AppUser

class CourseCreateForm(forms.ModelForm):
    class Meta:
        fields = ("title", "code")
        model = Course

class StudentCreateForm(forms.ModelForm):
    class Meta:
        fields = ("first_name", "middle_name", "last_name", "email", \
            "contact", "gender", "blood_group", "academic_level", \
            "academic_status", "academic_org", "academic_score",\
            "course", "intake", "shift", "remarks")
        model = Student