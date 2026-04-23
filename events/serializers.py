from rest_framework import serializers
from .models import Event
from accounts.serializers import UserSerializer
from tasks.serializers import TaskSerializer


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'event_type', 'user', 'task', 'metadata', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class EventListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'event_type', 'user_email', 'task_title', 'metadata', 'timestamp']
        read_only_fields = ['id', 'timestamp']
