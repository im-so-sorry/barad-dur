from rest_framework import serializers

from apps.social.models import NotificationService


class NotificationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationService
        fields = ("id", "user", "service", "value", "is_active")
        read_only_fields = ("user", )