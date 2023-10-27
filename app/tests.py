from django.test import TestCase
from app.models import Mapping

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
