from rest_framework import serializers

from apps.stream.models import Stream, Rule


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ("id", "project", "service", "description")


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "stream", "key", "value")