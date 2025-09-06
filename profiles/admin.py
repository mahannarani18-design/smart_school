# مسیر: profiles/admin.py

from django.contrib import admin
from .models import StudentProfile, TeacherProfile, ParentProfile
from attendance.models import AttendanceLog

@admin.action(description="ثبت ورود برای دانش‌آموزان انتخاب شده")
def mark_as_entered(modeladmin, request, queryset):
    for profile in queryset:
        AttendanceLog.objects.create(student=profile, event_type=AttendanceLog.EventType.ENTRY)

@admin.action(description="ثبت خروج برای دانش‌آموزان انتخاب شده")
def mark_as_exited(modeladmin, request, queryset):
    for profile in queryset:
        AttendanceLog.objects.create(student=profile, event_type=AttendanceLog.EventType.EXIT)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'grade', 'room', 'total_points') # <-- فیلد جدید اضافه شد
    readonly_fields = ('total_points',) # این فیلد نباید دستی ویرایش شود
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    actions = [mark_as_entered, mark_as_exited]

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty')

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')