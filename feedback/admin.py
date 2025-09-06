# مسیر: feedback/admin.py

from django.contrib import admin
from .models import Survey, SurveyQuestion

class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 1 # یک فیلد خالی برای افزودن سریع سوال

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    inlines = [SurveyQuestionInline]
    # مسیر: feedback/admin.py
# ADD this code to the END of the file

from .models import SurveyResponse, SurveyAnswer # این import را به بالای فایل اضافه کنید

class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer
    extra = 1

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'submitted_at')
    inlines = [SurveyAnswerInline]