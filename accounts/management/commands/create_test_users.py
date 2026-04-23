from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users for development'

    def handle(self, *args, **kwargs):
        # Create admin user
        if not User.objects.filter(email='admin@chronotasks.local').exists():
            User.objects.create_superuser(
                email='admin@chronotasks.local',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created: admin@chronotasks.local / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create regular user
        if not User.objects.filter(email='user@chronotasks.local').exists():
            User.objects.create_user(
                email='user@chronotasks.local',
                password='user123',
                first_name='Test',
                last_name='User',
                role='user'
            )
            self.stdout.write(self.style.SUCCESS('Regular user created: user@chronotasks.local / user123'))
        else:
            self.stdout.write(self.style.WARNING('Regular user already exists'))
