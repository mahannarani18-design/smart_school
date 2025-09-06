# مسیر: tasks/models.py

from django.db import models
from accounts.models import User

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'برای انجام'
        IN_PROGRESS = 'IN_PROGRESS', 'در حال انجام'
        DONE = 'DONE', 'انجام شده'

    title = models.CharField("عنوان وظیفه", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="محول شده به", related_name="tasks")
    due_date = models.DateField("تاریخ سررسید", null=True, blank=True)
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.TODO)
    created_at = models.DateTimeField("زمان ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "وظیفه"
        verbose_name_plural = "وظایف"
        ordering = ['due_date', 'created_at']

    def __str__(self):
        return self.title