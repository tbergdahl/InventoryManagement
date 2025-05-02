from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class TestUserManagement(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))

    def test_login_view(self):
        CustomUser.objects.create_user(username="testuser2", email="test2@example.com", password="testpass456")
        response = self.client.post(reverse('login_user'), {'username': 'testuser2', 'password': 'testpass456'})
        self.assertEqual(response.status_code, 302)  # Redirect after login (success)


