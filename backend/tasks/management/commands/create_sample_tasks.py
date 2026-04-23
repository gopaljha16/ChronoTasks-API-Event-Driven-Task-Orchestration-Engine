from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Task
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample tasks for testing'

    def handle(self, *args, **kwargs):
        # Get users
        try:
            admin = User.objects.get(email='admin@chronotasks.local')
            user = User.objects.get(email='user@chronotasks.local')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Please create test users first'))
            return

        # Sample tasks
        tasks_data = [
            {
                'title': 'Setup development environment',
                'description': 'Install all required dependencies and configure the project',
                'status': 'completed',
                'priority': 'high',
                'created_by': admin,
                'assigned_to': user,
            },
            {
                'title': 'Implement user authentication',
                'description': 'Create JWT-based authentication system',
                'status': 'completed',
                'priority': 'urgent',
                'created_by': admin,
                'assigned_to': user,
            },
            {
                'title': 'Build task management API',
                'description': 'Create CRUD endpoints for tasks with filtering',
                'status': 'in_progress',
                'priority': 'high',
                'created_by': admin,
                'assigned_to': user,
                'due_date': datetime.now() + timedelta(days=3),
            },
            {
                'title': 'Write API documentation',
                'description': 'Document all endpoints with examples',
                'status': 'pending',
                'priority': 'medium',
                'created_by': user,
                'assigned_to': user,
                'due_date': datetime.now() + timedelta(days=7),
            },
            {
                'title': 'Setup CI/CD pipeline',
                'description': 'Configure automated testing and deployment',
                'status': 'pending',
                'priority': 'low',
                'created_by': admin,
                'assigned_to': None,
                'due_date': datetime.now() + timedelta(days=14),
            },
        ]

        created_count = 0
        for task_data in tasks_data:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {task.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {task.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal tasks created: {created_count}'))
