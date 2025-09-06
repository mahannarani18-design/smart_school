# مسیر: omr/admin.py
from django.contrib import admin, messages
from .models import TestPaper, ScannedAnswerSheet
from academics.models import TestResult, Question, Answer, StudentAnswer
from .processor import process_omr_sheet

@admin.action(description="پردازش و نمره‌دهی پاسخنامه‌های انتخاب شده")
def process_and_score_sheets(modeladmin, request, queryset):
    successful_sheets = 0
    failed_sheets = 0

    for sheet in queryset.filter(status=ScannedAnswerSheet.Status.PENDING):
        if not sheet.student:
            failed_sheets += 1
            continue

        sheet.status = ScannedAnswerSheet.Status.PROCESSING
        sheet.save()

        try:
            processed_answers = process_omr_sheet(sheet.image.path)
            if not processed_answers:
                sheet.status = ScannedAnswerSheet.Status.ERROR
                sheet.save()
                failed_sheets += 1
                continue

            test = sheet.test_paper.test
            questions = list(test.questions.order_by('id'))
            answer_key = {}
            options_map = {}

            for i, question in enumerate(questions):
                options = list(question.answers.order_by('id'))
                options_map[i + 1] = options
                for j, option in enumerate(options):
                    if option.is_correct:
                        answer_key[i + 1] = j
                        break

            score = 0

            # ۱. نتیجه آزمون را ایجاد یا دریافت می‌کنیم
            test_result, created = TestResult.objects.get_or_create(
                student=sheet.student,
                test=test
            )
            # پاسخ‌های قبلی این دانش‌آموز در این آزمون را پاک می‌کنیم
            test_result.student_answers.all().delete()

            # ۲. پاسخ‌های دانش‌آموز را یکی یکی ذخیره می‌کنیم
            for question_num_str, student_choice_index in processed_answers.items():
                question_num = int(question_num_str)
                if student_choice_index != -1:
                    question_index = question_num - 1
                    if 0 <= question_index < len(questions):
                        question = questions[question_index]
                        options = options_map.get(question_num, [])

                        if 0 <= student_choice_index < len(options):
                            selected_option = options[student_choice_index]
                            # ذخیره پاسخ دانش‌آموز در مدل جدید
                            StudentAnswer.objects.create(
                                test_result=test_result,
                                question=question,
                                selected_answer=selected_option
                            )
                            # ۳. درستی پاسخ را بررسی و نمره را محاسبه می‌کنیم
                            if answer_key.get(question_num) == student_choice_index:
                                score += 1

            # ۴. ذخیره نهایی نمره در نتیجه آزمون
            test_result.score = score
            test_result.save()

            sheet.status = ScannedAnswerSheet.Status.COMPLETED
            sheet.save()
            successful_sheets += 1

        except Exception as e:
            print(f"Error processing sheet {sheet.id}: {e}")
            sheet.status = ScannedAnswerSheet.Status.ERROR
            sheet.save()
            failed_sheets += 1

    if successful_sheets > 0:
        modeladmin.message_user(request, f"{successful_sheets} پاسخنامه با موفقیت پردازش و نمره‌دهی شد.", messages.SUCCESS)
    if failed_sheets > 0:
        modeladmin.message_user(request, f"پردازش {failed_sheets} پاسخنامه با خطا مواجه شد.", messages.ERROR)


class ScannedAnswerSheetInline(admin.TabularInline):
    model = ScannedAnswerSheet
    extra = 0
    readonly_fields = ('student', 'status')

@admin.register(TestPaper)
class TestPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'test')
    inlines = [ScannedAnswerSheetInline]

@admin.register(ScannedAnswerSheet)
class ScannedAnswerSheetAdmin(admin.ModelAdmin):
    list_display = ('test_paper', 'student', 'status', 'uploaded_at')
    list_filter = ('status', 'test_paper')
    actions = [process_and_score_sheets]