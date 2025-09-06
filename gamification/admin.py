# مسیر: gamification/admin.py

from django.contrib import admin
from .models import PointLog

@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'points', 'reason', 'awarded_by', 'timestamp')
    list_filter = ('student', 'awarded_by', 'timestamp')
    search_fields = ('student__user__username', 'reason')

    def save_model(self, request, obj, form, change):
        # ثبت کاربری که امتیاز را اعطا کرده به صورت خودکار
        if not obj.awarded_by:
            obj.awarded_by = request.user
        super().save_model(request, obj, form, change)