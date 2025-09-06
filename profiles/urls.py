from django.urls import path
from .views import (
    StudentListAPIView, StudentDetailAPIView, StudentCreateAPIView, 
    StudentUpdateAPIView, StudentDeleteAPIView
)

urlpatterns = [
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('students/create/', StudentCreateAPIView.as_view(), name='student-create'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', StudentUpdateAPIView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', StudentDeleteAPIView.as_view(), name='student-delete'),
]