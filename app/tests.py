from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Mapping
from .forms import MappingForm
from .utils.parse_helpers import parse_excel
from .views import upload_to_fuseki
from unittest.mock import patch, MagicMock

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

    def test_upload_to_fuseki(self):
        """Test upload rdf to fuseki."""

        rdf_data = ("PREFIX ex: <http://example.org/>", "<ex:subject> <ex:predicate> <ex:object> .")
        # will raise a error if unsuccessful
        upload_to_fuseki(rdf_data)

    def test_parse_excel(self):
        """Test parse excel"""

        with patch('app.utils.parse_helpers.pd.read_excel') as mock_read_excel:
            # Mock DataFrame returned by pd.read_excel
            mock_df = MagicMock()
            mock_df.iterrows.return_value = iter([
                (0, {'name': 'John', 'age': 30}),
                (1, {'name': 'Jane', 'age': 25})
            ])
            mock_read_excel.return_value = mock_df

            # Call parse_excel
            name = 'test.xlsx'
            file = 'mock-path/to/test.xlsx'
            prefixes, triples = parse_excel(file, name)

            # Define expected output
            expected_prefixes = "PREFIX ex: <http://test.org/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"
            expected_triples = ("ex:0 ex:age 30 ;\n"
                                "    ex:name \"John\" .\n\n"
                                "ex:1 ex:age 25 ;\n"
                                "    ex:name \"Jane\" .")

            # Check if the prefixes and triples are as expected
            self.assertEqual(expected_prefixes.strip(), prefixes.strip())
            self.assertEqual(expected_triples.strip(), triples.strip())