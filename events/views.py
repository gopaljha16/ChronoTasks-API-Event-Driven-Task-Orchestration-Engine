from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsAdminUser
from .models import Event
from .serializers import EventSerializer, EventListSerializer
from .filters import EventFilter


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for events.
    Only admins can view events.
    """
    queryset = Event.objects.all().select_related('user', 'task')
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['event_type', 'user__email', 'task__title']
    ordering_fields = ['timestamp', 'event_type']
    ordering = ['-timestamp']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
