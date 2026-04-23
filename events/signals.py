from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from tasks.models import Task
from .models import Event


@receiver(post_save, sender=Task)
def create_task_event(sender, instance, created, **kwargs):
    """
    Create an event when a task is created or updated
    """
    if created:
        # Task was created
        Event.objects.create(
            event_type='TASK_CREATED',
            user=instance.created_by,
            task=instance,
            metadata={
                'task_id': instance.id,
                'title': instance.title,
                'status': instance.status,
                'priority': instance.priority,
                'assigned_to': instance.assigned_to.email if instance.assigned_to else None,
            }
        )
    else:
        # Task was updated
        # Check if task was completed
        if instance.status == 'completed' and hasattr(instance, '_previous_status'):
            if instance._previous_status != 'completed':
                Event.objects.create(
                    event_type='TASK_COMPLETED',
                    user=instance.created_by,
                    task=instance,
                    metadata={
                        'task_id': instance.id,
                        'title': instance.title,
                        'previous_status': instance._previous_status,
                        'new_status': instance.status,
                    }
                )
        else:
            # Regular update
            Event.objects.create(
                event_type='TASK_UPDATED',
                user=instance.created_by,
                task=instance,
                metadata={
                    'task_id': instance.id,
                    'title': instance.title,
                    'status': instance.status,
                    'priority': instance.priority,
                    'assigned_to': instance.assigned_to.email if instance.assigned_to else None,
                }
            )


@receiver(pre_save, sender=Task)
def store_previous_status(sender, instance, **kwargs):
    """
    Store the previous status before saving to detect completion
    """
    if instance.pk:
        try:
            previous = Task.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Task.DoesNotExist:
            instance._previous_status = None


@receiver(post_delete, sender=Task)
def create_task_deleted_event(sender, instance, **kwargs):
    """
    Create an event when a task is deleted
    """
    Event.objects.create(
        event_type='TASK_DELETED',
        user=instance.created_by,
        task=None,  # Task is deleted, so we can't reference it
        metadata={
            'task_id': instance.id,
            'title': instance.title,
            'status': instance.status,
            'priority': instance.priority,
        }
    )
