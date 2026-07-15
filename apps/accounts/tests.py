from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.accounts.models import ClientList, Profile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_list = ClientList.objects.create(
            company_name='Test Company',
            client_id='TC001',
            email_id='test@company.com'
        )
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword123'
        )
        self.user.profile.client = self.client_list
        self.user.profile.save()

    def test_profile_creation_signal(self):
        # When a user is created, a profile should be created automatically
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_login_view_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        logged_in = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(logged_in)
        
        # Test logout
        self.client.logout()
        # Ensure logout redirects (usually to root or login depending on settings)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
