# مسیر: maintenance/models.py

from django.db import models
from accounts.models import User

class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'باز'
        IN_PROGRESS = 'IN_PROGRESS', 'در دست بررسی'
        RESOLVED = 'RESOLVED', 'حل شده'
        CLOSED = 'CLOSED', 'بسته شده'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'پایین'
        MEDIUM = 'MEDIUM', 'متوسط'
        HIGH = 'HIGH', 'بالا'

    title = models.CharField("عنوان تیکت", max_length=200)
    description = models.TextField("شرح مشکل")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="گزارش دهنده", related_name="reported_tickets")
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField("اولویت", max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ارجاع به", related_name="assigned_tickets")
    created_at = models.DateTimeField("زمان ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title