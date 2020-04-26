from rest_framework import serializers

from apps.stream.models import Stream, Rule, Event


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ("id", "project", "service", "description")


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "key", "value", "service")

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").social_user.user
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "service", "tags", "event_type")


class FullEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "service", "payload", "tags", "event_type")


class StatsSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, allow_null=True)
    services = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, allow_null=True)

    from_date = serializers.DateTimeField(required=False, allow_null=True)
    to_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, attrs):
        self.tags = attrs.get('tags', [])
        self.services = attrs.get('services', [])
        self.from_date = attrs.get('from_date')
        self.to_date = attrs.get('to_date')

        return attrs
