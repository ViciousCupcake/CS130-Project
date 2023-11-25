"""
This file contains the form for the Mapping model. This form is used to create Mapping objects in the database. This file helps map the fields in the form to the fields in the database. This file is important because it allows us to create Mapping objects in the database without the need to write SQL queries.
"""


from django.forms import ModelForm
from app.models import Mapping
from django import forms

class MappingForm(ModelForm):
    """
    This class defines the form for the :model: `app.Mapping` model.
    """
    class Meta:
        """
        This class defines metadata for the form. 
        """
        model = Mapping
        fields = ["title", "graph_name", "description", "fuseki_relations", "excel_format"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'modify-form'}),
            'graph_name': forms.TextInput(attrs={'class': 'modify-form'}),
            'description': forms.TextInput(attrs={'class': 'modify-form'}),
            'fuseki_relations': forms.TextInput(attrs={'class': 'modify-form'}),
            'excel_format': forms.TextInput(attrs={'class': 'modify-form'}),
        }
