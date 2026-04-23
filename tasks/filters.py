from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.MultipleChoiceFilter(choices=Task.PRIORITY_CHOICES)
    assigned_to = filters.NumberFilter(field_name='assigned_to__id')
    created_by = filters.NumberFilter(field_name='created_by__id')
    due_date_after = filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date_before = filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Task
        fields = ['status', 'priority', 'assigned_to', 'created_by']
