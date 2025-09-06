# مسیر: kitchen/admin.py
from django.contrib import admin
from .models import FoodItem, Meal, MealLog

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'low_stock_threshold')
    search_fields = ('name',)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('date', 'meal_type', 'description')
    list_filter = ('date', 'meal_type')

@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'meal', 'timestamp')
    list_filter = ('meal__date', 'meal__meal_type')
    search_fields = ('student__user__username',)