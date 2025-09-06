# مسیر: gamification/models.py

from django.db import models
from profiles.models import StudentProfile
from accounts.models import User

class PointLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    points = models.IntegerField("امتیاز")
    reason = models.CharField("دلیل", max_length=255)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="اعطا شده توسط")
    timestamp = models.DateTimeField("زمان ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "گزارش امتیاز"
        verbose_name_plural = "گزارش‌های امتیاز"
        ordering = ['-timestamp']

    def __str__(self):
        points_str = f"+{self.points}" if self.points > 0 else str(self.points)
        return f"{points_str} امتیاز برای {self.student.user.username} به دلیل: {self.reason}"