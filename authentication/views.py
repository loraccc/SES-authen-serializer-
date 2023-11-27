from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")
    
    def post(self, request):
        req_username = request.POST.get('username')
        req_password = request.POST.get('password')

        if req_username and req_password:
            user = auth.authenticate(username=req_username, password=req_password)
            if user:
                if user.is_active:
                    messages.success(request, 'Welcome,  '+ user.username + " You're logged in!!")
                    return render(request, "students/index.html")
            return redirect("login")
        return redirect("login")

class LogoutView(View):
    def post(self, request):
        auth.logout
        messages.success(request, 'You are logged out')
        return redirect('login')

class RegisterView(View):
    def get(self, request):
        return render(request, "authentication/register.html")
    
    def post(self, request):
        req_username = request.POST.get('username')
        req_email = request.POST.get('email')
        req_password = request.POST.get('password')

        if not User.objects.filter(username=req_username).exists():
            if not User.objects.filter(email=req_email).exists():
                user = User.objects.create_user(username=req_username, email=req_email)
                user.set_password(req_password)
                user.is_active = False
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect("login")
            return redirect("register")
        return redirect("register")