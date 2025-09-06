# مسیر: maintenance/urls.py
from django.urls import path
from .views import TicketListCreateAPIView

urlpatterns = [
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
]