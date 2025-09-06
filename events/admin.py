# مسیر: events/admin.py

from django.contrib import admin
from .models import Event, EventRegistration

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1 # نمایش یک فرم خالی برای ثبت‌نام سریع

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'location', 'is_registration_open')
    list_filter = ('start_datetime', 'location', 'is_registration_open')
    search_fields = ('title', 'location')
    inlines = [EventRegistrationInline]

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'registration_date')
    list_filter = ('event',)
    search_fields = ('student__user__username', 'event__title')