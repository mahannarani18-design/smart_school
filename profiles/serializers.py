# مسیر: profiles/serializers.py
from rest_framework import serializers
from .models import StudentProfile
from accounts.serializers import UserSerializer
from academics.serializers import TestResultSerializer # حالا این import بدون مشکل کار می‌کند

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True, allow_null=True)
    testresult_set = TestResultSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'grade', 'room_number', 'total_points', 'testresult_set']

class StudentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'grade', 'room', 'username', 'password', 'first_name', 'last_name']

class StudentUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'grade', 'room', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return super().update(instance, validated_data)