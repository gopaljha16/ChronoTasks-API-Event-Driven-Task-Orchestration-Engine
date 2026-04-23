from celery import shared_task
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger('events')

User = get_user_model()


@shared_task(name='events.process_event')
def process_event(event_id):
    """
    Process an event asynchronously
    """
    from .models import Event
    
    try:
        event = Event.objects.select_related('user', 'task').get(id=event_id)
        logger.info(f"Processing event {event_id}: {event.event_type}")
        
        # Simulate event processing
        if event.event_type == 'TASK_CREATED':
            send_task_created_notification(event)
            update_analytics_counter('tasks_created')
        
        elif event.event_type == 'TASK_UPDATED':
            send_task_updated_notification(event)
            update_analytics_counter('tasks_updated')
        
        elif event.event_type == 'TASK_COMPLETED':
            send_task_completed_notification(event)
            update_analytics_counter('tasks_completed')
        
        elif event.event_type == 'TASK_DELETED':
            send_task_deleted_notification(event)
            update_analytics_counter('tasks_deleted')
        
        logger.info(f"Successfully processed event {event_id}")
        return f"Event {event_id} processed successfully"
    
    except Event.DoesNotExist:
        logger.error(f"Event {event_id} not found")
        return f"Event {event_id} not found"
    except Exception as e:
        logger.error(f"Error processing event {event_id}: {str(e)}")
        raise


@shared_task(name='events.send_notification')
def send_task_created_notification(event):
    """
    Send notification when task is created
    """
    logger.info(f"Sending task created notification for: {event.metadata.get('title')}")
    # Simulate sending email/push notification
    # In production, integrate with email service or push notification service
    return f"Notification sent for task: {event.metadata.get('title')}"


@shared_task(name='events.send_task_updated_notification')
def send_task_updated_notification(event):
    """
    Send notification when task is updated
    """
    logger.info(f"Sending task updated notification for: {event.metadata.get('title')}")
    return f"Update notification sent for task: {event.metadata.get('title')}"


@shared_task(name='events.send_task_completed_notification')
def send_task_completed_notification(event):
    """
    Send notification when task is completed
    """
    logger.info(f"Sending task completed notification for: {event.metadata.get('title')}")
    return f"Completion notification sent for task: {event.metadata.get('title')}"


@shared_task(name='events.send_task_deleted_notification')
def send_task_deleted_notification(event):
    """
    Send notification when task is deleted
    """
    logger.info(f"Sending task deleted notification for: {event.metadata.get('title')}")
    return f"Deletion notification sent for task: {event.metadata.get('title')}"


@shared_task(name='events.update_analytics')
def update_analytics_counter(counter_name):
    """
    Update analytics counters
    """
    logger.info(f"Updating analytics counter: {counter_name}")
    # In production, update Redis counters or analytics database
    # For now, just log the action
    return f"Analytics counter '{counter_name}' updated"


@shared_task(name='events.batch_process_events')
def batch_process_events(event_ids):
    """
    Process multiple events in batch
    """
    logger.info(f"Batch processing {len(event_ids)} events")
    results = []
    
    for event_id in event_ids:
        result = process_event.delay(event_id)
        results.append(result.id)
    
    return f"Batch processing initiated for {len(event_ids)} events"
