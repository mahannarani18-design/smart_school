# مسیر: attendance/admin.py

from django.contrib import admin
from .models import AttendanceLog, LeaveRequest

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'event_type', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('student__user__username',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('student__user__username',)
    # برای سادگی، فعلا همه فیلدها قابل ویرایش هستند
    # در آینده می‌توانیم منطق تایید و رد کردن را هوشمندتر کنیم