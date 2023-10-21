from django.forms import ModelForm
from app.models import Mapping

class MappingForm(ModelForm):
    class Meta:
        model = Mapping
        fields = ["title", "description", "fuseki_query", "excel_format"]
