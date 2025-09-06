from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import TestResult, Subject, Question, Answer
from .serializers import (
    TestResultSerializer, SubjectSerializer, QuestionSerializer, FileUploadSerializer
)
import fitz
import google.generativeai as genai
from decouple import config
import json

class TestResultListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.select_related('student__user', 'test__subject').all()

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.prefetch_related('answers').all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'difficulty', 'source', 'question_type']

class GenerateQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        subject = serializer.validated_data['subject']

        try:
            doc = fitz.open(stream=file.read(), filetype='pdf')
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            if not text.strip():
                return Response({"error": "فایل PDF فاقد متن بود."}, status=status.HTTP_400_BAD_REQUEST)

            GOOGLE_API_KEY = config('GOOGLE_API_KEY')
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            شما یک طراح سوال حرفه‌ای برای درس '{subject.name}' هستی.
            بر اساس متن زیر، 5 سوال چهارگزینه‌ای استاندارد طراحی کن.
            خروجی را فقط و فقط در فرمت JSON به صورت لیستی از آبجکت‌ها ارائه بده.
            هر آبجکت باید شامل کلیدهای "question_text", "answers" باشد.
            کلید "answers" باید لیستی از آبجکت‌ها باشد که هر کدام شامل "answer_text" و "is_correct" (boolean) است.
            متن:
            ---
            {text[:4000]}
            ---
            """

            response = model.generate_content(prompt)
            cleaned_response = response.text.strip().replace('`', '').replace('json', '')
            questions_data = json.loads(cleaned_response)

            for q_data in questions_data:
                question = Question.objects.create(subject=subject, question_text=q_data['question_text'], created_by=request.user)
                for ans_data in q_data['answers']:
                    Answer.objects.create(question=question, **ans_data)

            return Response({"message": f"{len(questions_data)} سوال با موفقیت تولید و ذخیره شد."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"یک خطای پیش‌بینی نشده رخ داد: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)