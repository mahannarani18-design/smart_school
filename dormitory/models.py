# مسیر: dormitory/models.py

from django.db import models

class Room(models.Model):
    room_number = models.CharField("شماره اتاق", max_length=10, unique=True)
    floor = models.IntegerField("طبقه")
    capacity = models.PositiveSmallIntegerField("ظرفیت")
    description = models.TextField("توضیحات", null=True, blank=True)

    class Meta:
        verbose_name = "اتاق"
        verbose_name_plural = "اتاق‌ها"
        ordering = ['floor', 'room_number']

    def __str__(self):
        return f"اتاق {self.room_number} - طبقه {self.floor}"