# مسیر: wellness/models.py

from django.db import models
from profiles.models import StudentProfile
from accounts.models import User

class MoodTracker(models.Model):
    class MoodChoice(models.TextChoices):
        HAPPY = 'HAPPY', '😊 خوشحال'
        NEUTRAL = 'NEUTRAL', '😐 معمولی'
        SAD = 'SAD', '😔 ناراحت'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    mood = models.CharField("حالت روحی", max_length=10, choices=MoodChoice.choices)
    notes = models.TextField("یادداشت (اختیاری)", blank=True, null=True)
    date = models.DateField("تاریخ", auto_now_add=True)

    class Meta:
        verbose_name = "گزارش حالت روحی"
        verbose_name_plural = "گزارش‌های حالات روحی"
        ordering = ['-date']

    def __str__(self):
        return f"حالت روحی {self.student.user.username} در تاریخ {self.date}"

class CounselingSession(models.Model):
    class StatusChoice(models.TextChoices):
        REQUESTED = 'REQUESTED', 'درخواست شده'
        SCHEDULED = 'SCHEDULED', 'زمان‌بندی شده'
        COMPLETED = 'COMPLETED', 'تکمیل شده'
        CANCELED = 'CANCELED', 'لغو شده'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="مشاور")
    session_datetime = models.DateTimeField("تاریخ و ساعت جلسه")
    notes = models.TextField("یادداشت‌های جلسه (محرمانه)", blank=True)
    status = models.CharField("وضعیت", max_length=20, choices=StatusChoice.choices, default=StatusChoice.REQUESTED)

    class Meta:
        verbose_name = "جلسه مشاوره"
        verbose_name_plural = "جلسات مشاوره"
        ordering = ['-session_datetime']

    def __str__(self):
        return f"جلسه مشاوره برای {self.student.user.username}"