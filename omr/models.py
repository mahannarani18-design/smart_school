# مسیر: omr/models.py

from django.db import models
from academics.models import Test
from profiles.models import StudentProfile

class TestPaper(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="آزمون مرتبط")
    title = models.CharField("عنوان برگه آزمون", max_length=200, help_text="مثال: آزمون فیزیک پایه دهم - کلاس ۱۰۱")

    class Meta:
        verbose_name = "برگه آزمون"
        verbose_name_plural = "برگه‌های آزمون"

    def __str__(self):
        return self.title

def get_upload_path(instance, filename):
    # فایل‌ها در مسیری مثل media/test_papers/1/answersheet.jpg ذخیره می‌شوند
    return f'test_papers/{instance.test_paper.id}/{filename}'

class ScannedAnswerSheet(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'در انتظار پردازش'
        PROCESSING = 'PROCESSING', 'در حال پردازش'
        COMPLETED = 'COMPLETED', 'پردازش کامل شد'
        ERROR = 'ERROR', 'خطا در پردازش'

    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE, verbose_name="برگه آزمون")
    image = models.ImageField("تصویر پاسخنامه", upload_to=get_upload_path)
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دانش‌آموز شناسایی شده")
    status = models.CharField("وضعیت پردازش", max_length=20, choices=Status.choices, default=Status.PENDING)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "پاسخنامه اسکن شده"
        verbose_name_plural = "پاسخنامه‌های اسکن شده"

    def __str__(self):
        return f"پاسخنامه برای {self.test_paper.title}"