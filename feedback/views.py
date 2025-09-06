# مسیر: feedback/views.py
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Survey
from .serializers import SurveySerializer

class SurveyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(is_active=True)