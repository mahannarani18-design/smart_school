from django.db import models
from django.utils import timezone
from profiles.models import StudentProfile
from accounts.models import User

class Subject(models.Model):
    name = models.CharField("نام درس", max_length=100)
    description = models.TextField("توضیحات", blank=True, null=True)

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"

    def __str__(self):
        return self.name

class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MC', 'چهار گزینه‌ای'
        TRUE_FALSE = 'TF', 'صحیح / غلط'
        SHORT_ANSWER = 'SA', 'پاسخ کوتاه'
        ESSAY = 'ES', 'تشریحی'

    class DifficultyLevel(models.TextChoices):
        EASY = 'EASY', 'آسان'
        MEDIUM = 'MEDIUM', 'متوسط'
        HARD = 'HARD', 'دشوار'

    class Source(models.TextChoices):
        KONKUR = 'KONKUR', 'کنکور سراسری'
        GHALAMCHI = 'GHALAMCHI', 'آزمون قلم‌چی'
        FINAL_EXAM = 'FINAL', 'امتحان نهایی'
        CUSTOM = 'CUSTOM', 'تالیفی'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="درس")
    question_text = models.TextField("متن سوال")
    question_type = models.CharField("نوع سوال", max_length=2, choices=QuestionType.choices, default=QuestionType.MULTIPLE_CHOICE)
    difficulty = models.CharField("سطح دشواری", max_length=10, choices=DifficultyLevel.choices, default=DifficultyLevel.MEDIUM)
    source = models.CharField("منبع سوال", max_length=20, choices=Source.choices, default=Source.CUSTOM)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ایجاد شده توسط")

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"
    def __str__(self):
        return self.question_text[:50] + "..."

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="سوال")
    answer_text = models.CharField("متن پاسخ", max_length=255)
    is_correct = models.BooleanField("پاسخ صحیح است؟", default=False)
    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ‌ها"
    def __str__(self):
        return self.answer_text

class Test(models.Model):
    title = models.CharField("عنوان آزمون", max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="درس")
    questions = models.ManyToManyField(Question, verbose_name="سوالات", blank=True)
    duration_minutes = models.PositiveIntegerField("مدت زمان (دقیقه)", default=60)

    class Meta:
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون‌ها"
    def __str__(self):
        return self.title

class TestSession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="آزمون")
    start_time = models.DateTimeField("زمان شروع", auto_now_add=True)
    end_time = models.DateTimeField("زمان پایان", null=True, blank=True)
    is_finished = models.BooleanField("پایان یافته؟", default=False)

    class Meta:
        verbose_name = "جلسه آزمون"
        verbose_name_plural = "جلسات آزمون"
    def __str__(self):
        return f"جلسه آزمون {self.test.title} برای {self.student.user.username}"

class TestResult(models.Model):
    test_session = models.OneToOneField(TestSession, on_delete=models.CASCADE, verbose_name="جلسه آزمون")
    score = models.FloatField("نمره کسب شده", null=True, blank=True)

    class Meta:
        verbose_name = "نتیجه آزمون"
        verbose_name_plural = "نتایج آزمون‌ها"
    def __str__(self):
        return f"نتیجه برای {self.test_session}"

class StudentAnswer(models.Model):
    test_session = models.ForeignKey(TestSession, related_name='student_answers', on_delete=models.CASCADE, verbose_name="جلسه آزمون")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="سوال")
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پاسخ انتخاب شده")
    essay_answer = models.TextField("پاسخ تشریحی", null=True, blank=True)

    class Meta:
        verbose_name = "پاسخ دانش‌آموز"
        verbose_name_plural = "پاسخ‌های دانش‌آموزان"
        unique_together = ('test_session', 'question')
    def __str__(self):
        return f"پاسخ به سوال {self.question.id} در {self.test_session}"