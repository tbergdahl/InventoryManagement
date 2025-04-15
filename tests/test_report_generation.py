from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from apps.inventory.models import InventoryItem, PerishableInventoryItem

class ReportGenerationTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Add a regular inventory item
        self.item_regular = InventoryItem.objects.create(
            name="Wrench",
            category="Tools",
            count=15
        )

        # Add a low-stock item
        self.item_low = InventoryItem.objects.create(
            name="Screwdriver",
            category="Tools",
            count=5
        )

        # Add a perishable item
        self.item_perishable = PerishableInventoryItem.objects.create(
            name="Milk",
            category="Dairy",
            count=12,
            expiry_date=datetime.now().date() + timedelta(days=3)
        )

    def test_generate_inventory_summary(self):
        response = self.client.post(reverse('reports_page'), {
            'report_type': 'inventory_summary'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrench")
        self.assertContains(response, "Screwdriver")
        self.assertContains(response, "Milk")

    def test_generate_low_stock_report(self):
        response = self.client.post(reverse('reports_page'), {
            'report_type': 'low_stock'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Screwdriver")
        self.assertNotContains(response, "Wrench")

    def test_generate_expiring_soon_report(self):
        response = self.client.post(reverse('reports_page'), {
            'report_type': 'expiring_soon'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milk")

    def test_generate_pdf_output(self):
        response = self.client.post(reverse('reports_page'), {
            'report_type': 'inventory_summary',
            'download_pdf': '1'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=', response['Content-Disposition'])
        self.assertTrue(len(response.content) > 100)  # crude check that it's not empty

    def test_generate_category_filtered(self):
        response = self.client.post(reverse('reports_page'), {
            'report_type': 'inventory_summary',
            'category': 'Tools'
        })

        self.assertContains(response, "Wrench")
        self.assertContains(response, "Screwdriver")
        self.assertNotContains(response, "Milk")
