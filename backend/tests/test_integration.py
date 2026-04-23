from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from events.models import Event

User = get_user_model()


class IntegrationTests(TestCase):
    """
    Integration tests for complete workflows
    """
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
    
    def test_complete_task_workflow(self):
        """Test complete task lifecycle"""
        self.client.force_authenticate(user=self.user)
        
        # 1. Create task
        response = self.client.post('/api/tasks/', {
            'title': 'Integration Test Task',
            'description': 'Test Description',
            'status': 'pending',
            'priority': 'high'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.data['id']
        
        # Verify event was created
        self.assertTrue(Event.objects.filter(
            event_type='TASK_CREATED',
            task_id=task_id
        ).exists())
        
        # 2. Update task
        response = self.client.patch(f'/api/tasks/{task_id}/', {
            'status': 'in_progress'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update event
        self.assertTrue(Event.objects.filter(
            event_type='TASK_UPDATED',
            task_id=task_id
        ).exists())
        
        # 3. Complete task
        response = self.client.patch(f'/api/tasks/{task_id}/mark_completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        
        # Verify completion event
        self.assertTrue(Event.objects.filter(
            event_type='TASK_COMPLETED',
            task_id=task_id
        ).exists())
        
        # 4. Delete task
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion event
        self.assertTrue(Event.objects.filter(
            event_type='TASK_DELETED',
            metadata__task_id=task_id
        ).exists())
    
    def test_user_authentication_flow(self):
        """Test complete authentication flow"""
        # 1. Register new user
        response = self.client.post('/api/auth/register/', {
            'email': 'newuser@test.com',
            'password': 'NewPass123!',
            'password2': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        
        access_token = response.data['tokens']['access']
        refresh_token = response.data['tokens']['refresh']
        
        # 2. Use access token to access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Refresh token
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_admin_event_access(self):
        """Test admin can access events while regular user cannot"""
        # Create a task to generate events
        Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        
        # Regular user should not access events
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should access events
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
    
    def test_task_filtering_and_search(self):
        """Test task filtering and search functionality"""
        self.client.force_authenticate(user=self.user)
        
        # Create multiple tasks
        Task.objects.create(
            title='High Priority Task',
            status='pending',
            priority='high',
            created_by=self.user
        )
        Task.objects.create(
            title='Low Priority Task',
            status='completed',
            priority='low',
            created_by=self.user
        )
        
        # Filter by status
        response = self.client.get('/api/tasks/?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data['results']:
            self.assertEqual(task['status'], 'pending')
        
        # Filter by priority
        response = self.client.get('/api/tasks/?priority=high')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data['results']:
            self.assertEqual(task['priority'], 'high')
        
        # Search
        response = self.client.get('/api/tasks/?search=High')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
