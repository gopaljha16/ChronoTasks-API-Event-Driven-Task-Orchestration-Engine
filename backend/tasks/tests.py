from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

User = get_user_model()


class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        
        # Create tasks
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            status='pending',
            priority='high',
            created_by=self.user1,
            assigned_to=self.user1
        )
        
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            status='in_progress',
            priority='medium',
            created_by=self.user2,
            assigned_to=self.user2
        )
    
    def test_create_task(self):
        """Test creating a task"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'pending',
            'priority': 'low'
        }
        
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
        
        # Verify task was created with correct user
        task = Task.objects.get(id=response.data['id'])
        self.assertEqual(task.created_by, self.user1)
    
    def test_list_tasks(self):
        """Test listing tasks"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should only see their own task
        self.assertEqual(response.data['count'], 1)
    
    def test_admin_sees_all_tasks(self):
        """Test admin can see all tasks"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_update_task(self):
        """Test updating a task"""
        self.client.force_authenticate(user=self.user1)
        
        data = {'status': 'completed'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
    
    def test_delete_task(self):
        """Test deleting a task"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())
    
    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.get('/api/tasks/?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_search_tasks(self):
        """Test searching tasks"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.get('/api/tasks/?search=Task 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_my_tasks_endpoint(self):
        """Test my_tasks custom endpoint"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get('/api/tasks/my_tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_mark_completed_endpoint(self):
        """Test mark_completed custom action"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.patch(f'/api/tasks/{self.task1.id}/mark_completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
    
    def test_unauthorized_access(self):
        """Test unauthorized access is denied"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
