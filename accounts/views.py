# مسیر: accounts/views.py
from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import User
from .serializers import UserSerializer
from profiles.models import StudentProfile
from dormitory.models import Room
from maintenance.models import Ticket
from events.models import Event

class UserListAPIView(ListAPIView):
    # ... (بدون تغییر)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class DashboardStatsAPIView(APIView):
    # ... (بدون تغییر)
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # ... (منطق قبلی بدون تغییر)
        student_count = StudentProfile.objects.count()
        room_count = Room.objects.count()
        open_tickets_count = Ticket.objects.filter(status='OPEN').count()
        upcoming_events_count = Event.objects.filter(start_datetime__gte=timezone.now()).count()
        stats = {
            'student_count': student_count,
            'room_count': room_count,
            'open_tickets_count': open_tickets_count,
            'upcoming_events_count': upcoming_events_count,
        }
        return Response(stats)

class StudentsByGradeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # گروه‌بندی دانش‌آموزان بر اساس پایه و شمارش تعداد هر گروه
        data = StudentProfile.objects.values('grade').annotate(count=Count('id')).order_by('grade')
        return Response(data)