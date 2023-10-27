from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import Mapping

class ExampleTestCase(TestCase):
    def test_example(self):
        """Example test case."""

        self.assertEqual(2, 1+1)

    def test_delete_model(self):
        """Test that a model can be deleted."""

        # Create admin user
        user = User.objects.create_user(username='admin', password='admin')

        client = Client()
        client.login(username='admin', password='admin')

        # Create a mapping
        Mapping.objects.create(title='test', description='test', fuseki_query='test', excel_format='{"test": "test"}')
        client.post('/delete/', {'id': 1})

        # Check that the mapping was deleted
        self.assertEqual(Mapping.objects.count(), 0)
