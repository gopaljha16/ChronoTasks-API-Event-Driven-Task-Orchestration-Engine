from django.core.management.base import BaseCommand
from django.core.cache import cache
from tasks.models import Task
from django.contrib.auth import get_user_model
import time

User = get_user_model()


class Command(BaseCommand):
    help = 'Test Redis cache functionality'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Testing Redis cache...'))
        
        # Test 1: Basic cache operations
        self.stdout.write('\n1. Testing basic cache operations...')
        cache.set('test_key', 'test_value', 60)
        value = cache.get('test_key')
        if value == 'test_value':
            self.stdout.write(self.style.SUCCESS('✓ Basic cache set/get works'))
        else:
            self.stdout.write(self.style.ERROR('✗ Basic cache failed'))
        
        # Test 2: Cache expiration
        self.stdout.write('\n2. Testing cache expiration...')
        cache.set('expire_test', 'value', 1)
        time.sleep(2)
        value = cache.get('expire_test')
        if value is None:
            self.stdout.write(self.style.SUCCESS('✓ Cache expiration works'))
        else:
            self.stdout.write(self.style.ERROR('✗ Cache expiration failed'))
        
        # Test 3: Cache deletion
        self.stdout.write('\n3. Testing cache deletion...')
        cache.set('delete_test', 'value', 60)
        cache.delete('delete_test')
        value = cache.get('delete_test')
        if value is None:
            self.stdout.write(self.style.SUCCESS('✓ Cache deletion works'))
        else:
            self.stdout.write(self.style.ERROR('✗ Cache deletion failed'))
        
        # Test 4: Complex data caching
        self.stdout.write('\n4. Testing complex data caching...')
        complex_data = {
            'list': [1, 2, 3],
            'dict': {'key': 'value'},
            'string': 'test'
        }
        cache.set('complex_test', complex_data, 60)
        cached_data = cache.get('complex_test')
        if cached_data == complex_data:
            self.stdout.write(self.style.SUCCESS('✓ Complex data caching works'))
        else:
            self.stdout.write(self.style.ERROR('✗ Complex data caching failed'))
        
        # Test 5: Performance comparison
        if Task.objects.exists():
            self.stdout.write('\n5. Testing cache performance...')
            
            # Without cache
            start = time.time()
            tasks = list(Task.objects.all().select_related('created_by', 'assigned_to')[:10])
            db_time = time.time() - start
            
            # With cache
            cache_key = 'perf_test_tasks'
            cache.set(cache_key, tasks, 60)
            start = time.time()
            cached_tasks = cache.get(cache_key)
            cache_time = time.time() - start
            
            self.stdout.write(f'  Database query time: {db_time*1000:.2f}ms')
            self.stdout.write(f'  Cache retrieval time: {cache_time*1000:.2f}ms')
            speedup = db_time / cache_time if cache_time > 0 else 0
            self.stdout.write(self.style.SUCCESS(f'  ✓ Cache is {speedup:.1f}x faster'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All cache tests completed!'))
