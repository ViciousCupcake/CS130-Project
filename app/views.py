from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Mapping
from .forms import MappingForm
import pandas as pd

def index(request):
    return render(request, "app/index.html", {'data': 'Hello, world!'})

def list(request):
    mappings = Mapping.objects.all()
    return render(request, "app/list.html", {"mappings": mappings})

@login_required
def select_mapping(request):
    """View that allows Administrative users to pick a mapping to modify"""
    if request.method == 'GET':
        mappings = Mapping.objects.all()
        return render(request, "app/select_mapping.html", {'mappings': mappings})

@login_required
def modify_mapping(request, pk=None):
    """View that allows Administrative users to modify a mapping"""

    # The request method is GET if we are loading the webpage for the first time
    if request.method == 'GET':
        # Attempt to preload mapping information to form if it already exists in db
        try:
            mapping = Mapping.objects.get(pk=pk)
            form = MappingForm(instance=mapping)
        except Mapping.DoesNotExist:
            form = MappingForm()

        return render(request, "app/modify.html", {'form': form})
    # The request method is POST if user hits "submit"
    # Save the form data to the database
    else:
        if pk:
            mapping = Mapping.objects.get(pk=pk)
            form = MappingForm(request.POST, instance=mapping)
        else:
            form = MappingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "app/save_success.html", {'mapping_title': form.cleaned_data['title']})
        else:
            return render(request, "app/modify.html", {'form': form})

def upload(request):
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'excelFile' in request.FILES:
            uploaded_file = request.FILES['excelFile']
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
                num_rows = df.shape[0]
                file_name = uploaded_file.name
                file_content = uploaded_file.read()
                return render(request, "app/success.html", {'num_rows': num_rows})
            else:
                return render(request, "app/upload.html", {'error': 'Invalid file format'})
        else:
            return render(request, "app/upload.html", {'error': 'No file found'})
    elif request.method == 'GET':
        mappings = Mapping.objects.all()
        return render(request, "app/upload.html", {"mappings": mappings})
    else:
        return render(request, "app/upload.html", {"data": 'unresolved request'})
