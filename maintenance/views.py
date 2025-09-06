# مسیر: maintenance/views.py
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer, TicketCreateSerializer

class TicketListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.select_related('reported_by', 'assigned_to').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        # کاربر فعلی را به عنوان گزارش‌دهنده ثبت کن
        serializer.save(reported_by=self.request.user)