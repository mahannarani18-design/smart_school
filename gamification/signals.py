# مسیر: gamification/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import PointLog

@receiver([post_save, post_delete], sender=PointLog)
def update_student_total_points(sender, instance, **kwargs):
    """
    هر زمان یک رکورد PointLog ذخیره یا حذف شد،
    مجموع امتیازات دانش‌آموز مربوطه را دوباره محاسبه می‌کند.
    """
    student_profile = instance.student
    total_points = PointLog.objects.filter(student=student_profile).aggregate(Sum('points'))['points__sum']
    student_profile.total_points = total_points or 0 # اگر هیچ امتیازی نباشد، صفر در نظر بگیر
    student_profile.save()