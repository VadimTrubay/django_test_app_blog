from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
