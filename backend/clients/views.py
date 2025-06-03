from rest_framework import permissions, viewsets

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('created_at')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
