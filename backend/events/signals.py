from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from tasks.models import Task
from .models import Event
import logging

logger = logging.getLogger('events')

# Store old task state before save
_task_old_state = {}


@receiver(pre_save, sender=Task)
def store_old_task_state(sender, instance, **kwargs):
    """Store old task state before save"""
    if instance.pk:
        try:
            old_task = Task.objects.get(pk=instance.pk)
            _task_old_state[instance.pk] = {
                'status': old_task.status,
            }
        except Task.DoesNotExist:
            pass


@receiver(post_save, sender=Task)
def create_task_event(sender, instance, created, **kwargs):
    """
    Create event when task is created or updated
    """
    if created:
        # Task was just created
        event = Event.objects.create(
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
        # Trigger async processing
        try:
            from .tasks import process_event
            process_event.delay(event.id)
            logger.info(f"Queued async processing for event {event.id}")
        except Exception as e:
            logger.error(f"Failed to queue event processing: {str(e)}")
    else:
        # Task was updated
        # Check if status changed to completed
        old_state = _task_old_state.get(instance.pk, {})
        old_status = old_state.get('status')
        
        if old_status and old_status != 'completed' and instance.status == 'completed':
            event = Event.objects.create(
                event_type='TASK_COMPLETED',
                user=instance.created_by,
                task=instance,
                metadata={
                    'task_id': instance.id,
                    'title': instance.title,
                    'completed_at': str(instance.updated_at),
                }
            )
        else:
            # Regular update
            event = Event.objects.create(
                event_type='TASK_UPDATED',
                user=instance.created_by,
                task=instance,
                metadata={
                    'task_id': instance.id,
                    'title': instance.title,
                    'status': instance.status,
                    'priority': instance.priority,
                    'changes': 'Task updated',
                }
            )
        
        # Trigger async processing
        try:
            from .tasks import process_event
            process_event.delay(event.id)
            logger.info(f"Queued async processing for event {event.id}")
        except Exception as e:
            logger.error(f"Failed to queue event processing: {str(e)}")
        
        # Clean up old state
        if instance.pk in _task_old_state:
            del _task_old_state[instance.pk]


@receiver(post_delete, sender=Task)
def delete_task_event(sender, instance, **kwargs):
    """
    Create event when task is deleted
    """
    event = Event.objects.create(
        event_type='TASK_DELETED',
        user=instance.created_by,
        task=None,  # Task is deleted, so we can't reference it
        metadata={
            'task_id': instance.id,
            'title': instance.title,
            'status': instance.status,
            'priority': instance.priority,
            'deleted_at': str(instance.updated_at),
        }
    )
    
    # Trigger async processing
    try:
        from .tasks import process_event
        process_event.delay(event.id)
        logger.info(f"Queued async processing for event {event.id}")
    except Exception as e:
        logger.error(f"Failed to queue event processing: {str(e)}")
