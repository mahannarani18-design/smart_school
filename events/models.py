# مسیر: events/models.py

from django.db import models
from profiles.models import StudentProfile

class Event(models.Model):
    title = models.CharField("عنوان رویداد", max_length=200)
    description = models.TextField("توضیحات")
    start_datetime = models.DateTimeField("زمان شروع")
    end_datetime = models.DateTimeField("زمان پایان")
    location = models.CharField("مکان", max_length=150)
    is_registration_open = models.BooleanField("ثبت‌نام باز است؟", default=True)
    max_participants = models.PositiveIntegerField("حداکثر ظرفیت", null=True, blank=True, help_text="برای ظرفیت نامحدود، خالی بگذارید.")

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="رویداد")
    registration_date = models.DateTimeField("زمان ثبت‌نام", auto_now_add=True)

    class Meta:
        verbose_name = "ثبت‌نام رویداد"
        verbose_name_plural = "ثبت‌نام‌های رویداد"
        # هر دانش‌آموز فقط یک بار می‌تواند در یک رویداد ثبت‌نام کند
        unique_together = ('student', 'event')

    def __str__(self):
        return f"ثبت‌نام {self.student.user.username} برای {self.event.title}"