# مسیر: attendance/views.py
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceLog
from .serializers import AttendanceLogSerializer, AttendanceLogCreateSerializer

class AttendanceLogListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceLogSerializer
    queryset = AttendanceLog.objects.select_related('student__user').all()

class LogAttendanceAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceLogCreateSerializer
    # perform_create به صورت خودکار تردد را ثبت می‌کند