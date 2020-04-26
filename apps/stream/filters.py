import rest_framework_filters as filters
from django.contrib.postgres.fields import JSONField
from django_filters.constants import EMPTY_VALUES

from apps.stream.models import Event


class JSONFilter(filters.Filter):
    field_class = JSONField

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        return qs.filter(**value)


class EventFilter(filters.FilterSet):
    payload = JSONFilter
    ordering = filters.OrderingFilter(
        fields=(
            ('created', 'created'),
            ('modified', 'modified'),
        ),
    )
    tag = filters.CharFilter(field_name='tag', method='filter_tag')

    class Meta:
        model = Event
        fields = {
            'service': '__all__',
            'event_type': '__all__',
            'created': '__all__',
        }

    def filter_tag(self, qs, name, value):
        return qs.filter(tags__icontains=value)
