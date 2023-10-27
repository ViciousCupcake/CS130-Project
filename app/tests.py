from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class ExampleTestCase(TestCase):
    def test_example(self):
        """Example test case."""

        self.assertEqual(2, 1+1)

    def test_auth(self):
        """Test authentication."""

        user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

        signed_in_user = authenticate(username='test', password='test')
        self.assertEqual(user, signed_in_user)

    def test_auth_fail(self):
        """Test authentication failure."""

        user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='wrong_password')

        signed_in_user = authenticate(username='test', password='wrong_password')
        self.assertNotEqual(user, signed_in_user)
    
    def test_auth_reachable(self):
        """Test authentication page reachable."""

        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test logout."""

        User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
