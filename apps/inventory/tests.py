from django.test import TestCase
from django.urls import reverse
from .models import InventoryItem

class TestInventoryItem(TestCase):
    def test_item_creation(self):
        item = InventoryItem.objects.create(name="Milk", count=20)
        self.assertEqual(item.name, "Milk")
        self.assertEqual(item.count, 20)

class TestInventoryHome(TestCase):
    def test_inventory_home_status_code(self):
        response = self.client.get(reverse('inventory_home'))
        self.assertEqual(response.status_code, 200)
