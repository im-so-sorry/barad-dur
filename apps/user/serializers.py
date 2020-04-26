from rest_framework import serializers

from apps.stream.models import Stream, Rule
from apps.user.models import User, SocialUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "project", "service", "description")


class SocialUserSerializer(serializers.ModelSerializer):
    is_streaming = serializers.SerializerMethodField(method_name="resolve_is_streaming")

    class Meta:
        model = SocialUser
        fields = ("id", "username", "user", "sync_token", "service", "is_streaming")

    def resolve_is_streaming(self, instance, *args, **kwargs):
        return instance.user.is_streaming