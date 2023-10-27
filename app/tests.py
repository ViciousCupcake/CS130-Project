from django.test import TestCase
from .forms import MappingForm

class ExampleTestCase(TestCase):
    def test_example(self):
        """Example test case."""

        self.assertEqual(2, 1+1)

    def test_form_validation_fail(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test', 'fuseki_query': 'test', 'excel_format': 'test'})
        self.assertFalse(form.is_valid())

    def test_form_validation_success(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test', 'fuseki_query': 'test', 'excel_format': '{"test": "data"}'})
        self.assertTrue(form.is_valid())
