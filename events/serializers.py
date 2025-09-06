# مسیر: events/serializers.py

from rest_framework import serializers
from .models import Event, EventRegistration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_datetime', 'end_datetime', 'location']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['event'] # فقط ID رویداد را از فرانت‌اند دریافت می‌کنیم