from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'مدیر'
        STUDENT = 'STUDENT', 'دانش‌آموز'
        TEACHER = 'TEACHER', 'معلم'
        STAFF = 'STAFF', 'کارمند'
        PARENT = 'PARENT', 'والدین'

    role = models.CharField(
        "نقش",
        max_length=50,
        choices=Role.choices,
        default=Role.ADMIN
    )

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username