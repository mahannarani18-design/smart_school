# مسیر: events/urls.py

from django.urls import path
from .views import EventListAPIView, EventRegistrationAPIView

urlpatterns = [
    # مسیر '' به ریشه /api/events/ اشاره دارد
    path('', EventListAPIView.as_view(), name='event-list'), 

    # مسیر 'register/' به /api/events/register/ اشاره دارد
    path('register/', EventRegistrationAPIView.as_view(), name='event-register'),
]