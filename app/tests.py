from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Mapping
from .forms import MappingForm
from SPARQLWrapper import SPARQLWrapper, JSON
import app.fuseki_scripts as fs
import pandas as pd


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
        
    def test_create_sparql_graph(self):
        """Test creating a sparql graph."""
        fs.create_sparql_graph("Test_Graph")

        sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/query")
        sparql.setCredentials("admin", "postgres")
        sparql.setReturnFormat(JSON)
        sparql.setQuery("""
            PREFIX : <http://example/>
            SELECT ?s ?p ?o
            WHERE {
                GRAPH :Test_Graph {
                    ?s ?p ?o
                }
            }
        """)
        results = sparql.query().convert()
        self.assertEqual(len(results["results"]["bindings"]), 0)
        
        fs.remove_sparql_graph("Test_Graph")
        
    def test_remove_sparql_graph(self):
        """Test removing a sparql graph."""
        fs.create_sparql_graph("Test_Graph")
        fs.remove_sparql_graph("Test_Graph")

        sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/query")
        sparql.setCredentials("admin", "postgres")
        sparql.setReturnFormat(JSON)
        sparql.setQuery("""
            PREFIX : <http://example/>
            SELECT ?s ?p ?o
            WHERE {
                GRAPH :Test_Graph {
                    ?s ?p ?o
                }
            }
        """)
        results = sparql.query().convert()
        self.assertEqual(len(results["results"]["bindings"]), 0)
        
    def test_insert_pandas_dataframe_into_sparql_graph(self):
        """Test inserting a pandas dataframe into a sparql graph."""
        fs.create_sparql_graph("Test_Graph")
        
        # Create Mapping object
        mapping = Mapping(
            title="Test Mapping",
            description="Test description",
            fuseki_relations=[["Test_Attribute_1", "Test_Relation", "Test_Attribute_2"]],
            excel_format={"test": "format"}
        )
        mapping.save()
        
        data = {"Test_Attribute_1": ["Test_Value_1"], "Test_Attribute_2": ["Test_Value_2"]}
        df = pd.DataFrame(data)
        
        fs.insert_pandas_dataframe_into_sparql_graph("Test_Graph", "Test Mapping", df)

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