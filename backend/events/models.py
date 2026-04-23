from django.db import models
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('TASK_CREATED', 'Task Created'),
        ('TASK_UPDATED', 'Task Updated'),
        ('TASK_COMPLETED', 'Task Completed'),
        ('TASK_DELETED', 'Task Deleted'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['task', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.user.email} - {self.timestamp}"
