from django.test import TestCase, Client
from app.models import Mapping
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
import pandas as pd

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
        