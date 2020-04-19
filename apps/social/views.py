from rest_framework import viewsets

from apps.social.models import NotificationService
from apps.social.serializers import NotificationServiceSerializer


class NotificationServiceModelView(viewsets.ModelViewSet):
    queryset = NotificationService.objects.all()
    serializer_class = NotificationServiceSerializer
