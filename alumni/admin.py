# مسیر: alumni/admin.py
from django.contrib import admin
from .models import AlumniProfile

@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'graduation_year', 'university', 'major', 'occupation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'university', 'major')