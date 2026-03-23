from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser, PasswordReset
from unittest.mock import patch


class UserAuthTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_register_success(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser', 
            'email': 'different@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_requires_auth(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_profile_update_bio(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/auth/profile/', {'bio': 'Hello world'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Hello world')

    @patch('users.views.PasswordResetRequestView') 
    def test_password_reset_request_valid_email(self, mock_send):
        response = self.client.post('/api/auth/password-reset/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordReset.objects.filter(user=self.user).exists())

    def test_password_reset_request_invalid_email(self):
        response = self.client.post('/api/auth/password-reset/', {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm_success(self):
        token = PasswordReset.objects.create(
            user=self.user,
            token='validtoken123'
        )
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': 'validtoken123',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token.refresh_from_db()
        self.assertTrue(token.used)

    def test_password_reset_confirm_invalid_token(self):
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': 'invalidtoken',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_confirm_short_password(self):
        PasswordReset.objects.create(
            user=self.user,
            token='validtoken456'
        )
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': 'validtoken456',
            'password': 'short'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)