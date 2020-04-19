from rest_framework import viewsets

from apps.social.models import NotificationService
from apps.stream.models import Rule
from apps.stream.serializers import StreamSerializer, RuleSerializer


class StreamModelView(viewsets.ModelViewSet):
    queryset = NotificationService.objects.all()
    serializer_class = StreamSerializer


class RuleModelView(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        social = self.request.query_params.get("social")

        if social:
            qs = qs.filter(stream__service=social)

        social_user = self.request.social_user

        if not qs:
            return Rule.objects.none()

        qs = qs.filter(stream__project__owner=social_user.user)

        return qs
