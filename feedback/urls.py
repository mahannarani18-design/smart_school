# مسیر: feedback/urls.py
from django.urls import path
from .views import SurveyListAPIView

urlpatterns = [
    path('surveys/', SurveyListAPIView.as_view(), name='survey-list'),
]