import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

class UserManagementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user and a normal user
        self.admin_user = User.objects.create_user(
            username="adminuser", password="adminpass", email="admin@example.com",
            usertype=User.UType.ADMIN
        )
        self.normal_user = User.objects.create_user(
            username="normaluser", password="normalpass", email="normal@example.com",
            usertype=User.UType.NORMAL
        )

    def test_login_user_valid_credentials(self):
        url = reverse('login_user')
        form_data = {'username': 'adminuser', 'password': 'adminpass'}
        response = self.client.post(url, form_data)
        self.assertRedirects(response, reverse('two_factor'))
        session = self.client.session
        self.assertIn('two_factor_code', session)
        self.assertIn('two_factor_user_id', session)
        self.assertEqual(int(session['two_factor_user_id']), self.admin_user.id)
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Your authentication code is:", mail.outbox[0].body)


    def test_login_user_invalid_credentials(self):
        url = reverse('login_user')
        form_data = {'username': 'adminuser', 'password': 'wrongpass'}
        response = self.client.post(url, form_data)
        self.assertContains(response, "Invalid username or password")

    def test_two_factor_valid_code(self):
        session = self.client.session
        session['two_factor_code'] = '123456'
        session['two_factor_user_id'] = self.normal_user.id
        session.save()
        url = reverse('two_factor')
        response = self.client.post(url, {'code': '123456'}, follow=True)
        self.assertRedirects(response, reverse('inventory_page'))
        self.assertIn('_auth_user_id', self.client.session)


    def test_two_factor_invalid_code(self):
        session = self.client.session
        session['two_factor_code'] = '123456'
        session['two_factor_user_id'] = self.normal_user.id
        session.save()
        url = reverse('two_factor')
        response = self.client.post(url, {'code': '000000'})
        self.assertContains(response, "Invalid code. Please try again.")

    def test_direct_based_off_user_admin(self):
        self.client.login(username="adminuser", password="adminpass")
        url = reverse('direct_to_page')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('admin_dashboard'))


    def test_direct_based_off_user_normal(self):
        self.client.login(username="normaluser", password="normalpass")
        url = reverse('direct_to_page')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('inventory_page'))


    def test_manage_users_create_user(self):
        self.client.login(username="adminuser", password="adminpass")
        url = reverse('manage_users')
        form_data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'NORMAL',
            'create_user': 'create_user'
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertRedirects(response, reverse('manage_users'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_manage_users_delete_user(self):
        self.client.login(username="adminuser", password="adminpass")
        del_user = User.objects.create_user(
            username="deleteuser", password="deletepass", email="delete@example.com", usertype=User.UType.NORMAL
        )
        url = reverse('manage_users')
        response = self.client.post(url, {'delete_user': del_user.id}, follow=True)
        self.assertRedirects(response, reverse('manage_users'))
        self.assertFalse(User.objects.filter(username="deleteuser").exists())

    def test_logout_view(self):
        self.client.login(username="adminuser", password="adminpass")
        url = reverse('logout')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse('login_user'))
        self.assertNotIn('_auth_user_id', self.client.session)
