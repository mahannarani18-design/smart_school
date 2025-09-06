# مسیر: tasks/admin.py

from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status')
    list_filter = ('status', 'assigned_to', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')