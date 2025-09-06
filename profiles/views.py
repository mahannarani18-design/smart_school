from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import StudentProfile
from .serializers import StudentProfileSerializer, StudentCreateSerializer, StudentUpdateSerializer
from accounts.models import User

class StudentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'student_id']

    def get_queryset(self):
        return StudentProfile.objects.select_related('user', 'room').all()

class StudentDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.select_related('user', 'room').prefetch_related('testresult_set__test').all()

class StudentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCreateSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.pop('username')
        password = serializer.validated_data.pop('password')
        first_name = serializer.validated_data.pop('first_name', '')
        last_name = serializer.validated_data.pop('last_name', '')
        new_user = User.objects.create_user(
            username=username, password=password, first_name=first_name,
            last_name=last_name, role=User.Role.STUDENT
        )
        serializer.save(user=new_user)

class StudentUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentUpdateSerializer
    queryset = StudentProfile.objects.all()

class StudentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()