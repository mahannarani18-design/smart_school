# مسیر: accounts/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # فیلدهایی که می‌خواهیم در خروجی API نمایش داده شوند
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']