# مسیر: profiles/models.py

from django.db import models
from accounts.models import User
from dormitory.models import Room

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    student_id = models.CharField("شماره دانش‌آموزی", max_length=20, unique=True)
    grade = models.CharField("پایه تحصیلی", max_length=50)
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="اتاق"
    )
    total_points = models.IntegerField("مجموع امتیازات", default=0)

    class Meta:
        verbose_name = "پروفایل دانش‌آموز"
        verbose_name_plural = "پروفایل‌های دانش‌آموزان"

    def __str__(self):
        return f"دانش‌آموز: {self.user.get_full_name() or self.user.username}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    specialty = models.CharField("رشته تخصصی", max_length=100)

    class Meta:
        verbose_name = "پروفایل معلم"
        verbose_name_plural = "پروفایل‌های معلمان"

    def __str__(self):
        return f"معلم: {self.user.get_full_name() or self.user.username}"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    children = models.ManyToManyField(StudentProfile, verbose_name="فرزندان")

    class Meta:
        verbose_name = "پروفایل والدین"
        verbose_name_plural = "پروفایل‌های والدین"

    def __str__(self):
        return f"والدین: {self.user.get_full_name() or self.user.username}"