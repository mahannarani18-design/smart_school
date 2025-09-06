from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestResultListView, SubjectViewSet, QuestionViewSet, GenerateQuestionsAPIView

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('results/', TestResultListView.as_view(), name='result-list'),
    path('generate-questions/', GenerateQuestionsAPIView.as_view(), name='generate-questions'),
    path('', include(router.urls)),
]