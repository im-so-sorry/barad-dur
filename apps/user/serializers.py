from rest_framework import serializers

from apps.stream.models import Stream, Rule
from apps.user.models import User, SocialUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "project", "service", "description")


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ("id", "username", "user", "sync_token", "service")