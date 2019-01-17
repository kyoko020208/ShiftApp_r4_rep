from accounts.models import UserManager
from rest_framework import viewsets
from .models import Schedule
from .serializer import UserSerializer, ScheduleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserManager.objects.all()
    serializer_class = UserSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer