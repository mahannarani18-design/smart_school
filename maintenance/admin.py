# مسیر: maintenance/admin.py

from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'reported_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('title', 'description', 'reported_by__username')
    # فیلدهایی که در فرم ویرایش فقط خواندنی باشند
    readonly_fields = ('reported_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # اگر تیکت جدید است، کاربر فعلی را به عنوان گزارش دهنده ثبت کن
        if not obj.pk:
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)