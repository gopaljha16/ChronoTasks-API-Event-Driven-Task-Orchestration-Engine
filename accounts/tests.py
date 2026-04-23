from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """Test user can register"""
        data = self.user_data.copy()
        data['password2'] = data['password']
        
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        """Test user can login"""
        # Create user first
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        response = self.client.post('/api/auth/login/', {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login/', {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

