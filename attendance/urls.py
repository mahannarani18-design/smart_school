# مسیر: attendance/urls.py
from django.urls import path
from .views import AttendanceLogListAPIView, LogAttendanceAPIView

urlpatterns = [
    path('logs/', AttendanceLogListAPIView.as_view(), name='attendance-log-list'),
    path('log-event/', LogAttendanceAPIView.as_view(), name='log-attendance-event'),
]