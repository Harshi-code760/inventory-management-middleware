from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# from django.contrib.auth.models import User
from users.models import CustomUser
from .models import Item, Category
from unittest.mock import patch

class InventoryTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='tester', email='python@test.com', password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_prevent_negative_stock(self):
        item = Item.objects.create(name='Phone', quantity=10, owner=self.user)
        url = reverse('item-detail', args=[item.id])
        data = {'quantity': -5}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 10)

    def test_audit_history_creation(self):
        item = Item.objects.create(name='Charger', quantity=10, owner=self.user)
        url = reverse('item-detail', args=[item.id])
        self.client.patch(url, {'quantity': 15})

        item.refresh_from_db()

        self.assertEqual(item.history.count(), 1)
        self.assertEqual(item.history.first().old, 10)
        self.assertEqual(item.history.first().new, 15)

    def test_category_user_isolation(self):
        other = CustomUser.objects.create_user(email="other@test.com", username="otheruser", password="password")
        Category.objects.create(name="Private", owner=other)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 0)

    @patch('inventory.emails.SendGridAPIClient')
    def test_stock_alert(self, mock_sg):
        mock_sg.return_value.send.return_value.status_code = 202
        item = Item.objects.create(
            name="Widget", quantity=10, low_stock=5, owner=self.user
        )
        url = reverse('item-detail', args=[item.id])
        self.client.patch(url, {'quantity': 3})
        self.assertTrue(mock_sg.return_value.send.called)

    @patch('inventory.emails.SendGridAPIClient')
    def test_no_alert(self, mock_sg):
        item = Item.objects.create(
            name='Widget', quantity=10, low_stock=5, owner=self.user
        )
        url = reverse('item-detail', args=[item.id])
        self.client.patch(url, {'quantity': 8})
        self.assertFalse(mock_sg.return_value.send.called)