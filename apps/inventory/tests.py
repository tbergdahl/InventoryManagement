from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import InventoryItem

class TestInventoryItem(TestCase):
    def test_item_creation(self):
        item = InventoryItem.objects.create(
            name="Milk",
            category="dairy",
            count=20
        )
        self.assertEqual(item.name, "Milk")
        self.assertEqual(item.count, 20)
        self.assertEqual(item.category, "dairy")

class TestInventoryHome(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            usertype='ADMIN'   
        )
        self.client.login(username='testuser', password='testpass')

    def test_inventory_home_status_code(self):
        response = self.client.get(reverse('inventory_home'))
        self.assertEqual(response.status_code, 200)
