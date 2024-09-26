from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationLoginTest(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "yourpassword",
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        # First, register the user
        self.client.post(self.register_url, {
            "username": "testuser",
            "email": "test@example.com",
            "password": "yourpassword",
        }, format='json')

        # Now try to log in
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "yourpassword"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Check for access token
        self.assertIn('refresh', response.data)  # Check for refresh token
        print()