from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AppUser, Student, Course

class AdminUser(admin.ModelAdmin):
     list_display = ("full_name", "email", "password", "usertype", "contact")
     search_fields = ("full_name", "email",) 
     list_filter = ("full_name", "email",)

class AdminStudent(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name", "email","contact", "academic_level", "academic_status", "course","intake", "shift", "remarks")
    search_fields = ("first_name", "contact", "course",)       
    list_filter = ("first_name", "contact", "course",)


admin.site.register(AppUser, AdminUser)
admin.site.register(Course)
admin.site.register(Student, AdminStudent)

admin.site.index_title = "STUDENT EQUIRY SYSTEM"
admin.site.site_title = "Admin Panel"
admin.site.site_header = "Admin Panel"