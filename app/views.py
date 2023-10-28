from django.shortcuts import render

from django.http import HttpResponse
from .models import Mapping
from .forms import MappingForm
import pandas as pd

def index(request):
    return render(request, "app/index.html", {'data': 'Hello, world!'})

def list(request):
    mappings = Mapping.objects.all()
    return render(request, "app/list.html", {"mappings": mappings})

def import_mapping(request): 
    form = MappingForm(request.POST or None, request.FILES or None)
     
    if form.is_valid():
        form.save()
        return render(request, "app/save_success.html", {'mapping_title': form.cleaned_data['title']})
 
    return render(request, "app/import.html", {'form': form})

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

    return render(request, "app/upload.html", {'data': 'Hello, world!'})

