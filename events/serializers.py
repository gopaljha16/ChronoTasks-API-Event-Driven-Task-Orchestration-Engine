from rest_framework import serializers
from .models import Event
from accounts.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task_id = serializers.IntegerField(source='task.id', read_only=True, allow_null=True)
    task_title = serializers.CharField(source='task.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'event_type', 'user', 'task_id', 'task_title',
            'metadata', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
