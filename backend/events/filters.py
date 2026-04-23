from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    event_type = filters.MultipleChoiceFilter(choices=Event.EVENT_TYPE_CHOICES)
    user = filters.NumberFilter(field_name='user__id')
    task = filters.NumberFilter(field_name='task__id')
    timestamp_after = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    
    class Meta:
        model = Event
        fields = ['event_type', 'user', 'task']
