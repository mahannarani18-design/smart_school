# مسیر: alumni/models.py
from django.db import models
from accounts.models import User

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    graduation_year = models.PositiveIntegerField("سال فارغ‌التحصیلی")
    university = models.CharField("دانشگاه", max_length=150, blank=True)
    major = models.CharField("رشته تحصیلی", max_length=150, blank=True)
    occupation = models.CharField("شغل فعلی", max_length=150, blank=True)
    contact_email = models.EmailField("ایمیل تماس", blank=True)

    class Meta:
        verbose_name = "پروفایل دانش‌آموخته"
        verbose_name_plural = "پروفایل‌های دانش‌آموختگان"

    def __str__(self):
        return f"دانش‌آموخته: {self.user.get_full_name() or self.user.username}"