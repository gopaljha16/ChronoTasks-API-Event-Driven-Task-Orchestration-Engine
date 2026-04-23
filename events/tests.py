from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from .models import Event

User = get_user_model()


class EventTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
    
    def test_event_created_on_task_creation(self):
        """Test that an event is created when a task is created"""
        initial_count = Event.objects.count()
        
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            created_by=self.user
        )
        
        self.assertEqual(Event.objects.count(), initial_count + 1)
        event = Event.objects.latest('timestamp')
        self.assertEqual(event.event_type, 'TASK_CREATED')
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.task, task)
    
    def test_event_created_on_task_update(self):
        """Test that an event is created when a task is updated"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        
        initial_count = Event.objects.count()
        
        task.title = 'Updated Task'
        task.save()
        
        self.assertEqual(Event.objects.count(), initial_count + 1)
        event = Event.objects.latest('timestamp')
        self.assertEqual(event.event_type, 'TASK_UPDATED')
    
    def test_event_created_on_task_completion(self):
        """Test that a TASK_COMPLETED event is created when task is marked complete"""
        task = Task.objects.create(
            title='Test Task',
            status='pending',
            created_by=self.user
        )
        
        initial_count = Event.objects.count()
        
        task.status = 'completed'
        task.save()
        
        self.assertEqual(Event.objects.count(), initial_count + 1)
        event = Event.objects.latest('timestamp')
        self.assertEqual(event.event_type, 'TASK_COMPLETED')
    
    def test_event_created_on_task_deletion(self):
        """Test that an event is created when a task is deleted"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        
        initial_count = Event.objects.count()
        task_id = task.id
        
        task.delete()
        
        self.assertEqual(Event.objects.count(), initial_count + 1)
        event = Event.objects.latest('timestamp')
        self.assertEqual(event.event_type, 'TASK_DELETED')
        self.assertEqual(event.task, None)
        self.assertEqual(event.metadata['task_id'], task_id)
    
    def test_admin_can_list_events(self):
        """Test that admin can list events"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_regular_user_cannot_list_events(self):
        """Test that regular users cannot list events"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_filter_events_by_type(self):
        """Test filtering events by type"""
        # Create some tasks to generate events
        Task.objects.create(title='Task 1', created_by=self.user)
        Task.objects.create(title='Task 2', created_by=self.user)
        
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.get('/api/events/?event_type=TASK_CREATED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # All returned events should be TASK_CREATED
        for event in response.data['results']:
            self.assertEqual(event['event_type'], 'TASK_CREATED')
    
    def test_event_metadata_contains_task_info(self):
        """Test that event metadata contains task information"""
        task = Task.objects.create(
            title='Test Task',
            status='pending',
            priority='high',
            created_by=self.user
        )
        
        event = Event.objects.latest('timestamp')
        self.assertIn('task_id', event.metadata)
        self.assertIn('title', event.metadata)
        self.assertIn('status', event.metadata)
        self.assertIn('priority', event.metadata)
        self.assertEqual(event.metadata['title'], 'Test Task')
