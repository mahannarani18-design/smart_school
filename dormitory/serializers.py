# مسیر: dormitory/serializers.py

from rest_framework import serializers
from .models import Room
from profiles.serializers import StudentProfileSerializer

class RoomSerializer(serializers.ModelSerializer):
    assigned_students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'floor', 'capacity', 'description', 'assigned_students_count']

class RoomDetailSerializer(serializers.ModelSerializer):
    # با استفاده از related_name که جنگو به صورت خودکار می‌سازد (studentprofile_set)
    # لیست پروفایل‌های دانش‌آموزی متصل به این اتاق را نمایش می‌دهیم.
    studentprofile_set = StudentProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'floor', 'capacity', 'description', 'studentprofile_set']