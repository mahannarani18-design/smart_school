# مسیر: events/views.py

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer

class EventListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(is_registration_open=True).order_by('start_datetime')

class EventRegistrationAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventRegistrationSerializer

    def create(self, request, *args, **kwargs):
        # مطمئن شویم کاربر دانش‌آموز است
        try:
            student_profile = request.user.studentprofile
        except:
            return Response({'error': 'فقط دانش‌آموزان می‌توانند ثبت‌نام کنند.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # جلوگیری از ثبت‌نام تکراری
        event = serializer.validated_data['event']
        if EventRegistration.objects.filter(student=student_profile, event=event).exists():
            return Response({'error': 'شما قبلاً در این رویداد ثبت‌نام کرده‌اید.'}, status=status.HTTP_400_BAD_REQUEST)

        # ذخیره ثبت‌نام جدید
        self.perform_create(serializer, student_profile)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': 'ثبت‌نام با موفقیت انجام شد.'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, student_profile):
        serializer.save(student=student_profile)