from django.shortcuts import render, redirect, HttpResponse
from django.core.files.base import File
from django.contrib.auth.decorators import login_required
from SPARQLWrapper import SPARQLWrapper, POST
from .models import Mapping, GeneratedExcelFile
from .forms import MappingForm
from .utils.parse_helpers import parse_excel
import os
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

        return render(request, "app/modify.html", {'form': form, 'pk': pk})
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

@login_required
def delete_mapping(request):
    """View that allows Administrative users to delete a mapping"""
    if request.method == 'POST':
        mapping = Mapping.objects.get(pk=request.POST['id'])
        mapping.delete()
        return render(request, "app/delete_success.html", {'mapping_title': mapping.title})
    elif request.method == 'GET':
        # Redirect to home page
        return redirect('index')

def upload_to_fuseki(rdf_data):
    """Uploaded parsed data (rdf data) to fuseki"""

    sparql = SPARQLWrapper("http://fuseki:3030/mydataset/update")
    # Set the credentials for authentication
    sparql.setCredentials(os.getenv('FUSEKI_USER'), os.getenv('FUSEKI_PASSWORD'))
    sparql.setMethod(POST)
    sparql.setQuery(f"""
    {rdf_data[0]}
    INSERT DATA {{
        {rdf_data[1]}
    }}
    """)
    sparql.query()
    
def upload(request):
    """ Upload and parse an excel sheet"""

    if request.method == 'POST':
        if 'excelFile' in request.FILES:
            uploaded_file = request.FILES['excelFile']
            selected_mapping_id = request.POST['mapping']
            selected_mapping = Mapping.objects.get(pk=selected_mapping_id)
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                file_name = uploaded_file.name
                rdf_data = parse_excel(uploaded_file, file_name)
                # mapping scheme could apply here later on
                upload_to_fuseki(rdf_data)
                return render(request, "app/upload_success.html", {'file_name': file_name})
            else:
                return render(request, "app/upload.html", {'error': 'Invalid file format: an .xls or .xlsx file is expected'})
        else:
            return render(request, "app/upload.html", {'error': 'No file uploaded'})
    elif request.method == 'GET':
        mappings = Mapping.objects.all()
        return render(request, "app/upload.html", {"mappings": mappings})
    else:
        return render(request, "app/upload.html", {"data": 'unresolved request'})

def download(request):
    """Download an excel sheet"""

    # If user is accessing this page for the first time,
    # present the user with a list of mappings available.
    if request.method == 'GET':
        mappings = Mapping.objects.all()
        return render(request, "app/download.html", {"mappings": mappings})
    # If user has selected a mapping to download,
    # do the logic to convert fuseki to excel and then allow user to download file
    if request.method == 'POST':
        selected_mapping_id = request.POST['mapping']
        selected_mapping = Mapping.objects.get(pk=selected_mapping_id)
        # TODO: convert fuseki to excel according to the selected mapping
        # and then store it to a GeneratedExcelFile object, like so:
        with open('/code/hello-world.xlsx', 'rb') as f:
            file_model = GeneratedExcelFile(excel_file=File(f, name='hello-world.xlsx'))
            print(f.read())
            file_model.save()

        return render(request, "app/export-success.html", {'file_pk': file_model.pk, 'selected_mapping': selected_mapping})

def download_file(request, pk):
    """Download a preexisting excel file"""
    
    file_model = GeneratedExcelFile.objects.get(pk=pk)
    file_name = file_model.excel_file.name.split('/')[-1]
    response = HttpResponse(file_model.excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
