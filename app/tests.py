from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Mapping
from .forms import MappingForm

class EFITestCase(TestCase):
    """Test Cases for EFi App."""
    def test_saving_mapping_model(self):
        """Test saving a mapping model."""
        mapping = Mapping(
            title="Test Mapping",
            description="Test description",
            fuseki_query="Test query",
            excel_format={"test": "format"}
        )
        mapping.save()

        saved_mapping = Mapping.objects.all()[0]
        self.assertEqual(saved_mapping.title, "Test Mapping")
        self.assertEqual(saved_mapping.description, "Test description")
        self.assertEqual(saved_mapping.fuseki_query, "Test query")
        self.assertEqual(saved_mapping.excel_format, {"test": "format"})

    def test_form_validation_fail(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test', 'fuseki_query': 'test', 'excel_format': 'test'})
        self.assertFalse(form.is_valid())

    def test_form_validation_success(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test', 'fuseki_query': 'test', 'excel_format': '{"test": "data"}'})
        self.assertTrue(form.is_valid())

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
