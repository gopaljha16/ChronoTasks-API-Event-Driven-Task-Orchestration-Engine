from django.core.management.base import BaseCommand
from events.tasks import process_event, update_analytics_counter
from events.models import Event


class Command(BaseCommand):
    help = 'Test Celery task execution'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Testing Celery tasks...'))
        
        # Test analytics counter
        self.stdout.write('Testing analytics counter task...')
        result = update_analytics_counter.delay('test_counter')
        self.stdout.write(self.style.SUCCESS(f'Task queued: {result.id}'))
        
        # Test event processing if events exist
        if Event.objects.exists():
            event = Event.objects.first()
            self.stdout.write(f'Testing event processing for event {event.id}...')
            result = process_event.delay(event.id)
            self.stdout.write(self.style.SUCCESS(f'Task queued: {result.id}'))
        else:
            self.stdout.write(self.style.WARNING('No events found to test'))
        
        self.stdout.write(self.style.SUCCESS('\nCelery tasks queued successfully!'))
        self.stdout.write('Check Celery worker logs to see task execution')
