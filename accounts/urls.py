# مسیر: accounts/urls.py
from django.urls import path
from .views import UserListAPIView, DashboardStatsAPIView, StudentsByGradeAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('dashboard-stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('charts/students-by-grade/', StudentsByGradeAPIView.as_view(), name='chart-students-by-grade'),
]