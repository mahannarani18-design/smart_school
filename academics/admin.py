from django.contrib import admin
from .models import Subject, Question, Answer, Test, TestResult, StudentAnswer, TestSession

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'subject', 'question_type', 'difficulty', 'source')
    list_filter = ('subject', 'question_type', 'difficulty', 'source')
    inlines = [AnswerInline]
    search_fields = ('question_text',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    # خط زیر برای رفع خطا حذف شد
    # filter_horizontal = ('questions',)

# ثبت مدل‌های دیگر
admin.site.register(Subject)
admin.site.register(TestResult)
admin.site.register(StudentAnswer)
admin.site.register(TestSession)