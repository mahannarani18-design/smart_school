# مسیر: attendance/serializers.py
from rest_framework import serializers
from .models import AttendanceLog
from profiles.serializers import StudentProfileSerializer

class AttendanceLogSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    class Meta:
        model = AttendanceLog
        fields = ['id', 'student', 'timestamp', 'event_type', 'notes']

# سریالایزر جدید برای دریافت درخواست ثبت تردد
class AttendanceLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLog
        fields = ['student', 'event_type']