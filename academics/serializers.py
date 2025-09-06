from rest_framework import serializers
from .models import Subject, Question, Answer, Test, TestResult, StudentAnswer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        # id را حذف می‌کنیم تا در ساخت/ویرایش سوال بتوانیم گزینه‌ها را بدون id بفرستیم
        fields = ['answer_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'subject', 'question_text', 'difficulty', 'source', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.source = validated_data.get('source', instance.source)
        instance.save()

        answers_data = validated_data.get('answers')
        if answers_data is not None:
            instance.answers.all().delete()
            for answer_data in answers_data:
                Answer.objects.create(question=instance, **answer_data)

        return instance

class TestSerializer(serializers.ModelSerializer):
    # برای نمایش نام درس به جای ID آن
    subject = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Test
        fields = ['id', 'title', 'subject', 'questions']

class TestResultSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    test = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'student', 'test', 'score', 'completed_at']

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())