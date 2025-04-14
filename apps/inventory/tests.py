import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .forms import InventoryItemForm
from .models import InventoryItem, PerishableInventoryItem, NonPerishableInventoryItem
from django.contrib.auth import get_user_model

User = get_user_model()


# Form Tests
class InventoryItemFormTest(TestCase):
    def test_perishable_without_expiry(self):
        form_data = {
            'item_type': 'perishable',
            'name': 'Milk',
            'category': 'dairy',
            'count': 10,
            # 'expiry_date' left out on purpose (should give error)
        }
        form = InventoryItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('expiry_date', form.errors)

    def test_perishable_with_expiry(self):
        form_data = {
            'item_type': 'perishable',
            'name': 'Milk',
            'category': 'dairy',
            'count': 10,
            'expiry_date': '2025-04-15'
        }
        form = InventoryItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_non_perishable_without_expiry(self):
        form_data = {
            'item_type': 'non-perishable',
            'name': 'Canned Beans',
            'category': 'canned',
            'count': 20,
            'expiry_date': ''  # Empty is allowed
        }
        form = InventoryItemForm(data=form_data)
        self.assertTrue(form.is_valid())


# Model Tests
class InventoryItemModelTest(TestCase):
    def test_is_perishable_property(self):
        perishable = PerishableInventoryItem.objects.create(
            name="Yogurt",
            category="dairy",
            count=5,
            expiry_date="2025-04-10"
        )
        non_perishable = NonPerishableInventoryItem.objects.create(
            name="Canned Beans",
            category="canned",
            count=20
        )
        # For perishable the property should be True
        self.assertTrue(perishable.is_perishable)
        # For non-perishable the property should be False
        self.assertFalse(hasattr(non_perishable, 'expiry_date'))


# View Tests
class InventoryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin test user
        self.test_user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com",
            usertype=User.UType.ADMIN
        )
        # Login the test user
        self.client.login(username="testuser", password="testpass")

        # Create some test items
        PerishableInventoryItem.objects.create(
            name="Milk",
            category="dairy",
            count=10,
            expiry_date="2025-03-30"
        )
        PerishableInventoryItem.objects.create(
            name="Cheese",
            category="dairy",
            count=5,
            expiry_date="2025-04-01"
        )
        NonPerishableInventoryItem.objects.create(
            name="Beans",
            category="canned",
            count=20
        )

    def test_inventory_page_no_filter_default_sort(self):
        # Test that the inventory homepage orders items by newest added
        url = reverse('inventory_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milk")
        items = list(response.context['items'])
        self.assertEqual(items[0].name, "Beans")

    def test_sort_expiry(self):
        # Test that sorting by expiry date orders perishable items first and non-perishables last
        url = reverse('inventory_home') + "?sort=expiry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        items = list(response.context['items'])
        self.assertEqual(items[0].name, "Milk")
        self.assertEqual(items[1].name, "Cheese")
        self.assertEqual(items[2].name, "Beans")

    def test_create_inventory_item_view_perishable(self):
        # Test creating perishable item with create_inventory_item view
        url = reverse('create_item')
        form_data = {
            'item_type': 'perishable',
            'name': 'Yogurt',
            'category': 'dairy',
            'count': 6,
            'expiry_date': '2025-04-20'
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertRedirects(response, reverse('inventory_home'))
        self.assertTrue(PerishableInventoryItem.objects.filter(name='Yogurt').exists())

    def test_delete_inventory_item_view(self):
        # Create an item to delete
        item = PerishableInventoryItem.objects.create(
            name="Test Delete",
            category="dairy",
            count=1,
            expiry_date="2025-04-15"
        )
        url = reverse('delete_item', args=[item.id])
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('inventory_home'))
        self.assertFalse(PerishableInventoryItem.objects.filter(id=item.id).exists())
