from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Clear all cache entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear cache entries matching pattern (e.g., "task_*")',
        )

    def handle(self, *args, **options):
        pattern = options.get('pattern')
        
        if pattern:
            self.stdout.write(f'Clearing cache entries matching: {pattern}')
            try:
                cache.delete_pattern(pattern)
                self.stdout.write(self.style.SUCCESS(f'✓ Cleared cache pattern: {pattern}'))
            except AttributeError:
                self.stdout.write(self.style.ERROR('Pattern deletion not supported by cache backend'))
        else:
            self.stdout.write('Clearing all cache entries...')
            cache.clear()
            self.stdout.write(self.style.SUCCESS('✓ All cache cleared'))
