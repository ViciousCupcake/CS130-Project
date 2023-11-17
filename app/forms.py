from django.forms import ModelForm
from app.models import Mapping
from django import forms

class MappingForm(ModelForm):
    class Meta:
        model = Mapping
        fields = ["title", "graph_name", "description", "fuseki_relations", "excel_format"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'modify-form'}),
            'graph_name': forms.TextInput(attrs={'class': 'modify-form'}),
            'description': forms.TextInput(attrs={'class': 'modify-form'}),
            'fuseki_relations': forms.TextInput(attrs={'class': 'modify-form'}),
            'excel_format': forms.TextInput(attrs={'class': 'modify-form'}),
        }
