from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Mapping, Fuski_Relation, Fuski_Relations_Group
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
        
    def test_saving_fuski_relations_list_model(self):
        """Test saving a fuski relations list model."""
        relation1 = Fuski_Relation.objects.create(
            name="Test Relation",
            description="Test description",
            attribute1="Test Attribute 1",
            attribute2="Test Attribute 2",
        )
        relation2 = Fuski_Relation.objects.create(
            name="Test Relation 2",
            description="Test description 2",
            attribute1="Test Attribute 3",
            attribute2="Test Attribute 4",
        )
        
        relations_list = Fuski_Relations_Group.objects.create(
            name="Test Relations List",
            description="Test description",
        )
        relations_list.relations.add(relation1)
        relations_list.relations.add(relation2)
        
        saved_relations_list = Fuski_Relations_Group.objects.all()[0]
        self.assertEqual(saved_relations_list.name, "Test Relations List")
        self.assertEqual(saved_relations_list.description, "Test description")
        self.assertEqual(saved_relations_list.relations.all()[0], relation1)
        self.assertEqual(saved_relations_list.relations.all()[1], relation2)
        
    def test_saving_fuski_relation_model(self):
        """Test saving a fuski relation model."""
        relation = Fuski_Relation.objects.create(
            name="Test Relation",
            description="Test description",
            attribute1="Test Attribute 1",
            attribute2="Test Attribute 2",
        )
        
        saved_relation = Fuski_Relation.objects.all()[0]
        self.assertEqual(saved_relation.name, "Test Relation")
        self.assertEqual(saved_relation.description, "Test description")
        self.assertEqual(saved_relation.attribute1, "Test Attribute 1")
        self.assertEqual(saved_relation.attribute2, "Test Attribute 2")

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
