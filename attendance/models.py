# مسیر: attendance/models.py

from django.db import models
from profiles.models import StudentProfile
from accounts.models import User

class AttendanceLog(models.Model):
    class EventType(models.TextChoices):
        ENTRY = 'ENTRY', 'ورود'
        EXIT = 'EXIT', 'خروج'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    timestamp = models.DateTimeField("زمان ثبت", auto_now_add=True)
    event_type = models.CharField("نوع رویداد", max_length=10, choices=EventType.choices)
    notes = models.TextField("یادداشت", null=True, blank=True)

    class Meta:
        verbose_name = "گزارش تردد"
        verbose_name_plural = "گزارش‌های تردد"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student} - {self.get_event_type_display()} در {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class LeaveRequest(models.Model):
    class StatusType(models.TextChoices):
        PENDING = 'PENDING', 'در انتظار بررسی'
        APPROVED = 'APPROVED', 'تایید شده'
        REJECTED = 'REJECTED', 'رد شده'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    start_date = models.DateTimeField("تاریخ و ساعت شروع")
    end_date = models.DateTimeField("تاریخ و ساعت بازگشت")
    reason = models.TextField("دلیل مرخصی")
    status = models.CharField("وضعیت", max_length=10, choices=StatusType.choices, default=StatusType.PENDING)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تایید شده توسط")

    class Meta:
        verbose_name = "درخواست مرخصی"
        verbose_name_plural = "درخواست‌های مرخصی"
        ordering = ['-start_date']

    def __str__(self):
        return f"درخواست مرخصی برای {self.student}"