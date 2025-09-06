# مسیر: dormitory/admin.py

from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor', 'capacity')
    list_filter = ('floor',)
    search_fields = ('room_number',)