from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Mapping
from .forms import MappingForm
from .utils.parse_helpers import parse_excel
from .views import upload_to_fuseki
from unittest.mock import patch, MagicMock
from SPARQLWrapper import SPARQLWrapper, JSON
import app.fuseki_scripts as fs
import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO


class EFITestCase(TestCase):
    """Test Cases for EFi App."""

    def test_saving_mapping_model(self):
        """Test saving a mapping model."""
        mapping = Mapping(
            title="Test Mapping",
            description="Test description",
            fuseki_relations=[["Test Attribute 1", "Test Relation", "Test Attribute 2"]],
            excel_format={"test": "format"}
        )
        mapping.save()

        saved_mapping = Mapping.objects.all()[0]
        self.assertEqual(saved_mapping.title, "Test Mapping")
        self.assertEqual(saved_mapping.description, "Test description")
        self.assertEqual(saved_mapping.fuseki_relations, [["Test Attribute 1", "Test Relation", "Test Attribute 2"]])
        self.assertEqual(saved_mapping.excel_format, {"test": "format"})
        
    # def test_create_sparql_graph(self):
    #     """Test creating a sparql graph."""
    #     fs.create_sparql_graph("Test_Graph")

    #     sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/query")
    #     sparql.setCredentials("admin", "postgres")
    #     sparql.setReturnFormat(JSON)
    #     sparql.setQuery("""
    #         PREFIX : <http://example/>
    #         SELECT ?s ?p ?o
    #         WHERE {
    #             GRAPH :Test_Graph {
    #                 ?s ?p ?o
    #             }
    #         }
    #     """)
    #     results = sparql.query().convert()
    #     self.assertEqual(len(results["results"]["bindings"]), 0)
        
    #     fs.remove_sparql_graph("Test_Graph")
        
    # def test_remove_sparql_graph(self):
    #     """Test removing a sparql graph."""
    #     fs.create_sparql_graph("Test_Graph")
    #     fs.remove_sparql_graph("Test_Graph")

    #     sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/query")
    #     sparql.setCredentials("admin", "postgres")
    #     sparql.setReturnFormat(JSON)
    #     sparql.setQuery("""
    #         PREFIX : <http://example/>
    #         SELECT ?s ?p ?o
    #         WHERE {
    #             GRAPH :Test_Graph {
    #                 ?s ?p ?o
    #             }
    #         }
    #     """)
    #     results = sparql.query().convert()
    #     self.assertEqual(len(results["results"]["bindings"]), 0)
        
    # def test_insert_pandas_dataframe_into_sparql_graph(self):
    #     """Test inserting a pandas dataframe into a sparql graph."""
    #     fs.create_sparql_graph("Test_Graph")
        
    #     # Create Mapping object
    #     mapping = Mapping(
    #         title="Test Mapping",
    #         description="Test description",
    #         fuseki_relations=[["Test_Attribute_1", "Test_Relation", "Test_Attribute_2"]],
    #         excel_format={"test": "format"}
    #     )
    #     mapping.save()
        
    #     data = {"Test_Attribute_1": ["Test_Value_1"], "Test_Attribute_2": ["Test_Value_2"]}
    #     df = pd.DataFrame(data)
        
    #     fs.insert_pandas_dataframe_into_sparql_graph("Test_Graph", "Test Mapping", df)

    def test_delete_model(self):
        """Test that a model can be deleted."""

        # Create admin user
        user = User.objects.create_user(username='admin', password='admin')

        client = Client()
        client.login(username='admin', password='admin')

        # Create a mapping
        Mapping.objects.create(title='test', description='test', fuseki_relations='[["test", "test", "test"]]', excel_format='{"test": "test"}')
        client.post('/delete/', {'id': 1})

        # Check that the mapping was deleted
        self.assertEqual(Mapping.objects.count(), 0)
    def test_form_validation_fail(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test',
                           'fuseki_relations': 'test', 'excel_format': 'test'})
        self.assertFalse(form.is_valid())

    def test_form_validation_success(self):
        """Test Mapping ModelForm validation."""

        form = MappingForm(data={'title': 'test', 'description': 'test',
                           'fuseki_relations': '[["test", "test", "test"]]', 'excel_format': '{"test": "test"}'})
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

        signed_in_user = authenticate(
            username='test', password='wrong_password')
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

class UploadViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/upload.html')
        
    def test_invalid_post_request(self):
        response = self.client.post('/upload/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/upload.html')
        self.assertIn('error', response.context)

    def test_invalid_file_type(self):
        invalid_format = SimpleUploadedFile('test.txt', b'this is invalid format', content_type='text/plain')
        response = self.client.post('/upload/', {'excelFile': invalid_format})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/upload.html')
        self.assertIn('error', response.context)

    def test_unresolved_request_method(self):
        response = self.client.delete('/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/upload.html')
        self.assertIn('data', response.context)
        
    def test_valid_post_request(self):
        df = pd.DataFrame({'Data': [1, 2, 3]})
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        valid_excel = SimpleUploadedFile('valid.xlsx', excel_file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response = self.client.post('/upload/', {'excelFile': valid_excel})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/success.html')
        self.assertIn('num_rows', response.context)
