# مسیر: wellness/admin.py

from django.contrib import admin
from .models import MoodTracker, CounselingSession

@admin.register(MoodTracker)
class MoodTrackerAdmin(admin.ModelAdmin):
    list_display = ('student', 'mood', 'date')
    list_filter = ('mood', 'date', 'student')

@admin.register(CounselingSession)
class CounselingSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'counselor', 'session_datetime', 'status')
    list_filter = ('status', 'counselor', 'student')