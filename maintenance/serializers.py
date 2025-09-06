# مسیر: maintenance/serializers.py
from rest_framework import serializers
from .models import Ticket
from accounts.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    reported_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # کاربر گزارش‌دهنده به صورت خودکار ثبت می‌شود
        fields = ['title', 'description', 'priority', 'assigned_to']