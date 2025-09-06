# مسیر: accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from profiles.models import StudentProfile, TeacherProfile, ParentProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'پروفایل دانش‌آموزی'
    # اضافه کردن فیلد اتاق به اینلاین
    fields = ('student_id', 'grade', 'room')

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'پروفایل معلم'

class ParentProfileInline(admin.StackedInline):
    model = ParentProfile
    can_delete = False
    verbose_name_plural = 'پروفایل والدین'

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات سفارشی', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات سفارشی', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    inlines = []

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == User.Role.STUDENT:
                return [StudentProfileInline]
            elif obj.role == User.Role.TEACHER:
                return [TeacherProfileInline]
            elif obj.role == User.Role.PARENT:
                return [ParentProfileInline]
        return self.inlines

admin.site.register(User, CustomUserAdmin)