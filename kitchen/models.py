# مسیر: kitchen/models.py
from django.db import models
from profiles.models import StudentProfile

class FoodItem(models.Model):
    class Unit(models.TextChoices):
        KILOGRAM = 'KG', 'کیلوگرم'
        LITER = 'L', 'لیتر'
        NUMBER = 'NO', 'عدد'

    name = models.CharField("نام کالا", max_length=100)
    unit = models.CharField("واحد اندازه‌گیری", max_length=2, choices=Unit.choices)
    quantity = models.FloatField("موجودی فعلی")
    low_stock_threshold = models.FloatField("آستانه هشدار کسری", default=10.0)

    class Meta:
        verbose_name = "قلم غذایی"
        verbose_name_plural = "اقلام غذایی انبار"
    def __str__(self):
        return self.name

class Meal(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = 'B', 'صبحانه'
        LUNCH = 'L', 'ناهار'
        DINNER = 'D', 'شام'

    meal_type = models.CharField("وعده", max_length=1, choices=MealType.choices)
    date = models.DateField("تاریخ")
    description = models.CharField("شرح غذا", max_length=255)

    class Meta:
        verbose_name = "وعده غذایی"
        verbose_name_plural = "وعده‌های غذایی"
        unique_together = ('date', 'meal_type') # در هر روز از هر وعده فقط یکی داریم
    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.date}"

class MealLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="وعده غذایی")
    timestamp = models.DateTimeField("زمان ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "گزارش غذای مصرفی"
        verbose_name_plural = "گزارش‌های غذای مصرفی (ژتون)"
        unique_together = ('student', 'meal') # هر دانش‌آموز برای هر وعده فقط یک ژتون دارد
    def __str__(self):
        return f"ژتون {self.meal} برای {self.student.user.username}"