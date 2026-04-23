from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth import get_user_model
from core.cache import generate_cache_key, invalidate_task_cache
from core.throttling import BurstRateThrottle, TaskCreateThrottle

User = get_user_model()


class CacheUtilsTests(TestCase):
    def setUp(self):
        cache.clear()
    
    def test_generate_cache_key(self):
        """Test cache key generation"""
        key1 = generate_cache_key('test', 'arg1', param='value')
        key2 = generate_cache_key('test', 'arg1', param='value')
        key3 = generate_cache_key('test', 'arg2', param='value')
        
        # Same inputs should generate same key
        self.assertEqual(key1, key2)
        
        # Different inputs should generate different keys
        self.assertNotEqual(key1, key3)
    
    def test_cache_operations(self):
        """Test basic cache operations"""
        from core.cache import get_cached_data, set_cached_data, delete_cached_data
        
        # Set and get
        set_cached_data('test_key', {'data': 'value'}, 60)
        data = get_cached_data('test_key')
        self.assertEqual(data, {'data': 'value'})
        
        # Delete
        delete_cached_data('test_key')
        data = get_cached_data('test_key')
        self.assertIsNone(data)
    
    def test_invalidate_task_cache(self):
        """Test task cache invalidation"""
        # Set some cache entries
        cache.set('task_detail:1', 'data', 60)
        cache.set('user_tasks:1', 'data', 60)
        
        # Invalidate
        invalidate_task_cache(task_id=1, user_id=1)
        
        # Verify deletion
        self.assertIsNone(cache.get('task_detail:1'))
        self.assertIsNone(cache.get('user_tasks:1'))


class ThrottlingTests(TestCase):
    def test_burst_rate_throttle(self):
        """Test burst rate throttle configuration"""
        throttle = BurstRateThrottle()
        self.assertEqual(throttle.scope, 'burst')
    
    def test_task_create_throttle(self):
        """Test task creation throttle"""
        throttle = TaskCreateThrottle()
        self.assertEqual(throttle.rate, '100/hour')
