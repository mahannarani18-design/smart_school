# File Path: dormitory/views.py
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer, RoomDetailSerializer

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoomDetailSerializer
        return RoomSerializer

    def get_queryset(self):
        if self.action == 'list':
            # --- This line is corrected ---
            return Room.objects.annotate(
                assigned_students_count=Count('studentprofile_set') # Correct name
            ).all()
        return super().get_queryset().prefetch_related('studentprofile_set__user')