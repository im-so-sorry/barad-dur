from collections import defaultdict
from typing import Dict, List

from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.social.models import NotificationService
from apps.stream.filters import EventFilter
from apps.stream.models import Rule, Event
from apps.stream.serializers import StreamSerializer, RuleSerializer, EventSerializer, FullEventSerializer, \
    StatsSerializer
from apps.stream import tasks


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
            qs = qs.filter(service=social)

        social_user = self.request.social_user

        if not qs:
            return Rule.objects.none()

        qs = qs.filter(user=social_user.user)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        tasks.add_rule(instance.key, instance.value)

    @action(methods=['delete'], detail=False, url_path='remove_rule', url_name='remove_rule')
    def remove_rule(self, request, *args, **kwargs):
        key = request.data.get("key")
        social = request.data.get("social")

        rule = self.get_queryset().filter(key=key, service=social, user=self.request.social_user.user).first()

        if not rule:
            return Response(status=status.HTTP_404_NOT_FOUND)

        rule.delete()

        return Response("ok", status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = EventFilter

    def get_serializer_class(self):
        return {
            "retrieve": FullEventSerializer
        }.get(self.action, super().get_serializer_class())

    def get_queryset(self):
        qs = super().get_queryset()
        rules = self.request.social_user.user.rules.get_queryset()

        tags = list(rules.values_list("key", flat=True).all())
        return qs.filter(tags__overlap=tags)

    def _count(self, tags: Dict[str, List[Event]]):
        res = defaultdict(dict)

        for tag, events in tags.items():
            res[tag]["count"] = defaultdict(int)
            res[tag]["total"] = len(events)

            for event in events:
                res[tag]["count"][event.event_type] += 1

        return res

    @action(methods=['post'], detail=False, url_path='stats', url_name='stats')
    def stats(self, request, *args, **kwargs):
        serializer = StatsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qs = self.get_queryset()

        if serializer.tags:
            qs = qs.filter(tags__overlap=serializer.tags)

        if serializer.from_date:
            qs = qs.filter(created__gte=serializer.from_date)
        if serializer.to_date:
            qs = qs.filter(created__lte=serializer.to_date)

        tags = defaultdict(list)

        for event in qs:
            for tag in event.tags:
                if not serializer.tags or tag in serializer.tags:
                    tags[tag].append(event)

        result = {
            "total": qs.count(),
            "rules": [
                {
                    "tag": tag,
                    **event,
                }
                for tag, event in self._count(tags).items()
            ]
        }

        return Response(result)
