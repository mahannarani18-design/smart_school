# مسیر: feedback/serializers.py
from rest_framework import serializers
from .models import Survey, SurveyQuestion

class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ['id', 'question_text', 'question_type']

class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_at', 'questions']