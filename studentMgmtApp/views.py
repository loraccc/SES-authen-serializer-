from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# Create your views here.
from django.shortcuts import render, redirect
from .forms import StudentCreateForm, CourseCreateForm, UserRegisterForm, UserLoginForm
from .models import Course, Student, AppUser
from django.core.mail import send_mail

#  package for api
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer, AppUserSerializer, CourseSerializer
from rest_framework.request import Request
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# api views with Class Based views
class StudentApiView(APIView):
    # get method to get list of data i.e students' list
    def get(self, request):
        student_list = Student.objects.all() # model object
        serializer = StudentSerializer(student_list, many=True) # serializing model obj
        return Response(serializer.data, status=status.HTTP_200_OK) # returning response
    
    def post(self, request):
        data = {
            "first_name": request.data.get("first_name"),
            "middle_name":request.data.get("middle_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "contact": request.data.get("contact"),
            "gender": request.data.get("gender"),
            "blood_group": request.data.get("blood_group"),
            "academic_level": request.data.get("academic_level"),
            "academic_status": request.data.get("academic_status"),
            "academic_org": request.data.get("academic_org"),
            "academic_score": request.data.get("academic_score"),
            "course": request.data.get("course_id"),
            "intake": request.data.get("intake"),
            "shift": request.data.get("shift"),
            "remarks": request.data.get("remarks"),
        }

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentIdApiView(APIView):

    def get_object(self, id):
        try:
            data = Student.objects.get(id=id)
            return data
        except Student.DoesNotExist:
            return None
    
    def get(self, request, id):
        std_instance = self.get_object(id)

        if not std_instance:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(std_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        std_instance = self.get_object(id)

        if not std_instance:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "first_name": request.data.get("first_name"),
            "middle_name":request.data.get("middle_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "contact": request.data.get("contact"),
            "gender": request.data.get("gender"),
            "blood_group": request.data.get("blood_group"),
            "academic_level": request.data.get("academic_level"),
            "academic_status": request.data.get("academic_status"),
            "academic_org": request.data.get("academic_org"),
            "academic_score": request.data.get("academic_score"),
            "course": request.data.get("course_id"),
            "intake": request.data.get("intake"),
            "shift": request.data.get("shift"),
            "remarks": request.data.get("remarks"),
        }
        
        serializer = StudentSerializer(instance=std_instance, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        std_instance = self.get_object(id)

        if not std_instance:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

        std_instance.delete()
        return Response({"msg": "Data deleted"}, status=status.HTTP_200_OK)
            
# Create your views here.
# def user_register(request):
#     reg_form = UserRegisterForm()
#     context = {"form": reg_form}
#     if request.method == "POST":
#         user_form_data = UserRegisterForm(request.POST)
#         if user_form_data.is_valid():
#             user_form_data.save()
#             send_mail(
#                 "User Registration", # subject
#                 "Congratulations! Your account has been created", # message
#                 "c4crypt@gmail.com", # sender
#                 [request.POST.get('email')] # receiver
#             )
#             return redirect("users.login")
#         else:
#             return redirect("users.register")
#     return render(request, "users/register.html", context)


def user_register(request):
    reg_form = UserCreationForm()

    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)  # Log in the user after registration
            return redirect("students.index")

    context = {"form": reg_form}
    return render(request, "users/register.html", context)

def user_login(request):
    login_form = AuthenticationForm()
    context = {"form": login_form}

    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            # Authentication successful, log in the user
            user = login_form.get_user()
            login(request, user)
            return redirect("students.index")
        else:
            # Authentication failed, redirect to login page
            return redirect("users.login")

    return render(request, "users/login.html", context)
# def user_login(request):
#     login_form = UserLoginForm()
#     context = {"form": login_form}

#     if request.method == "POST":
#         req_email = request.POST.get("email")
#         req_password = request.POST.get("password")

#         # Authenticate using the custom user model
#         user = authenticate(request, email=req_email, password=req_password)

#         if user is not None:
#             print("Login successful. Redirecting to students.index")
#             login(request, user)
#             return redirect("students.index")
#         else:
#             print("Login failed. Redirecting to users.login")
#             return redirect("users.login")

#     return render(request, "users/login.html", context)


# @login_required(login_url="/authentication/login")
# @login_required(login_url="/ses/users/login/") 
@login_required(login_url='/users/login/')  
def student_index(request):
    # if not request.session.has_key("session_email"):
    #     return redirect("users.login")
    std_list = Student.objects.all()
    context = {"std_list": std_list}
    return render(request, "students/index.html", context)

# @login_required(login_url="/authentication/login")
@login_required(login_url='/users/login/')  

def student_create(request):
    # if not request.session.has_key("session_email"):
    #     return redirect("users.login")
    std_create_form = StudentCreateForm()
    context = {
        "temp_form": std_create_form
    }

    if request.method == "POST":
        course = Course.objects.get(id=request.POST.get("course"))
        std_obj = Student()
        std_obj.first_name = request.POST.get("first_name")
        std_obj.middle_name = request.POST.get("middle_name")
        std_obj.last_name = request.POST.get("last_name")
        std_obj.email = request.POST.get("email")
        std_obj.contact = request.POST.get("contact")
        std_obj.gender = request.POST.get("gender")
        std_obj.blood_group = request.POST.get("blood_group")
        std_obj.academic_level = request.POST.get("academic_level")
        std_obj.academic_status = request.POST.get("academic_status")
        std_obj.academic_org = request.POST.get("academic_org")
        std_obj.academic_score = request.POST.get("academic_score")
        std_obj.course = course
        std_obj.intake = request.POST.get("intake")
        std_obj.shift = request.POST.get("shift")
        std_obj.remarks = request.POST.get("remarks")
        std_obj.save()
        subject = 'User Created Successfully'
        message = 'Congratulations! Your account has been created.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['carolacharya1@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
        context.setdefault("msg", "Student Added Successfully")

    return render(request, "students/create.html", context)
    # /Users/carolacharya/Desktop/MYSES/studentMgmtProj/templates/students/create.html
# @login_required(login_url="/authentication/login")
def student_update(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    if request.method == "POST":
        course = Course.objects.get(id=request.POST.get("course_id"))
        std_obj = Student.objects.get(id=request.POST.get('id'))
        std_obj.first_name = request.POST.get("first_name")
        std_obj.middle_name = request.POST.get("middle_name")
        std_obj.last_name = request.POST.get("last_name")
        std_obj.email = request.POST.get("email")
        std_obj.contact = request.POST.get("contact")
        std_obj.gender = request.POST.get("gender")
        std_obj.blood_group = request.POST.get("blood_group")
        std_obj.academic_level = request.POST.get("academic_level")
        std_obj.academic_status = request.POST.get("academic_status")
        std_obj.academic_org = request.POST.get("academic_org")
        std_obj.academic_score = request.POST.get("academic_score")
        std_obj.course = course
        std_obj.intake = request.POST.get("intake")
        std_obj.shift = request.POST.get("shift")
        std_obj.remarks = request.POST.get("remarks")
        std_obj.save()
    
    return redirect("students.index")

def student_show(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Student.objects.get(id=id)
    context = {"data": data}
    return render(request, "students/show.html", context)

def student_edit(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Student.objects.get(id=id)
    courses = Course.objects.all()
    context = {"data": data, "courses": courses}
    return render(request, "students/edit.html", context)

def student_delete(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Student.objects.get(id=id)
    data.delete()
    return redirect("students.index")