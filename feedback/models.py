# مسیر: feedback/models.py

from django.db import models

class Survey(models.Model):
    title = models.CharField("عنوان نظرسنجی", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    is_active = models.BooleanField("فعال است؟", default=True, help_text="کاربران فقط می‌توانند به نظرسنجی‌های فعال پاسخ دهند.")
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "نظرسنجی"
        verbose_name_plural = "نظرسنجی‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class SurveyQuestion(models.Model):
    class QuestionType(models.TextChoices):
        TEXT = 'TEXT', 'متنی'
        RATING = 'RATING', 'امتیازی (۱ تا ۵)'
        # در آینده می‌توان انواع بیشتری اضافه کرد

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name="نظرسنجی")
    question_text = models.CharField("متن سوال", max_length=255)
    question_type = models.CharField("نوع سوال", max_length=10, choices=QuestionType.choices, default=QuestionType.TEXT)

    class Meta:
        verbose_name = "سوال نظرسنجی"
        verbose_name_plural = "سوالات نظرسنجی"

    def __str__(self):
        return self.question_text
    # مسیر: feedback/models.py
# ADD this code to the END of the file

from accounts.models import User # این import را به بالای فایل اضافه کنید

# ... (کلاس‌های Survey و SurveyQuestion در بالای این قسمت قرار دارند) ...

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="نظرسنجی")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر پاسخ‌دهنده")
    submitted_at = models.DateTimeField("زمان ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "پاسخ نظرسنجی"
        verbose_name_plural = "پاسخ‌های نظرسنجی"
        unique_together = ('survey', 'user') # جلوگیری از ثبت پاسخ تکراری

    def __str__(self):
        return f"پاسخ {self.user.username} به نظرسنجی '{self.survey.title}'"

class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, related_name='answers', on_delete=models.CASCADE, verbose_name="مجموعه پاسخ")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, verbose_name="سوال")
    text_answer = models.TextField("پاسخ متنی", blank=True, null=True)
    rating_answer = models.PositiveSmallIntegerField("پاسخ امتیازی", blank=True, null=True)

    class Meta:
        verbose_name = "پاسخ سوال"
        verbose_name_plural = "پاسخ‌های سوالات"

    def __str__(self):
        return f"پاسخ به سوال: {self.question.question_text[:30]}..."