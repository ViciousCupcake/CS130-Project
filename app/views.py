"""
This file contains the views for the app. This represents the backend logic of
this application. Please refer to app.urls for the urls of this application.
"""


from django.shortcuts import render, redirect, HttpResponse
from django.core.files.base import File
from django.contrib.auth.decorators import login_required
from SPARQLWrapper import SPARQLWrapper, POST
from app.fuseki_scripts import fuseki_relations_to_sparql_response, fuseki_response_to_DataFrame, insert_pandas_dataframe_into_sparql_graph
from .models import Mapping, GeneratedExcelFile
from .forms import MappingForm
from .utils.visual_helpers import visualize_relations
import os
from io import BytesIO
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    """
    Returns True if the user is an admin, False otherwise.

    :param user: The user to check.
    :type user: User
    :return: True if the user is an admin, False otherwise.
    """
    return user.is_authenticated and user.is_superuser

def index(request):
    """
    Renders the index page.

    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered index page.
    """
    return render(request, "app/index.html", {'data': 'Hello, world!'})

def list(request):
    """
    Renders the list page, which lists all mappings.

    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered list page.
    """
    mappings = Mapping.objects.all()
    return render(request, "app/list.html", {"mappings": mappings})

def search_mappings(request):
    """
    Allows users to search for a mapping
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The mappings that match the search query.
    """

    query = request.GET.get('q', '')
    if query:
        mappings = Mapping.objects.filter(title__icontains=query)
    else:
        mappings = Mapping.objects.all()

    return mappings

def visualize_mapping(request):
    """
    Visualize a mapping based on user input
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered visualization page.
    """

    mappings = Mapping.objects.all()
    if request.method == 'POST':

        # Query the Mapping model to get the desired mapping
        try:
            selected_mapping_id = request.POST['mapping']
            mapping = Mapping.objects.get(pk=selected_mapping_id)
            relations = mapping.fuseki_relations

            # Visualize the mapping and save it as an image
            visualize_relations(relations, 'static/images/my_graph.png')

            return render(request, 'app/visualization_result.html', {'image_path': 'images/my_graph.png'})
        except KeyError:
            return render(request, "app/visualize_mapping.html", {"mappings": mappings, 'error': 'Please select a mapping'})

    # For a GET request, just render the form
    return render(request, 'app/visualize_mapping.html', {"mappings": mappings})

@login_required
@user_passes_test(is_admin)
def select_mapping(request):
    """
    View that allows Administrative users to pick a mapping to modify.
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered select_mapping page.
    """
    if request.method == 'GET':
        mappings = Mapping.objects.all()
        return render(request, "app/select_mapping.html", {'mappings': mappings})

@login_required
@user_passes_test(is_admin)
def modify_mapping(request, pk=None):
    """
    View that allows Administrative users to modify a mapping
    
    :param request: The request object.
    :type request: HttpRequest
    :param pk: The primary key of the mapping to modify.
    :type pk: int
    :return: The rendered modify page.
    """
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
            return render(request, "app/modify.html", {'form':form, 'mapping_title': form.cleaned_data['title']})
        else:
            return render(request, "app/modify.html", {'form': form})

@login_required
@user_passes_test(is_admin)  
def delete_mapping(request):
    """
    View that allows Administrative users to delete a mapping
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered select_mapping page.
    """
    if request.method == 'POST':
        mapping = Mapping.objects.get(pk=request.POST['id'])
        mapping.delete()
        mappings = Mapping.objects.all()
        return render(request, "app/select_mapping.html", {'mappings': mappings, 'mapping_title': mapping.title})
    elif request.method == 'GET':
        # Redirect to home page
        return redirect('index')

def upload_to_fuseki(rdf_data):
    """
    Uploaded parsed data (rdf data) to fuseki
    
    :param rdf_data: The rdf data to upload to fuseki.
    :type rdf_data: list
    :return: None
    """

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
    """
    Upload and parse an excel sheet
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered upload page.
    """

    if request.method == 'POST':
        mappings = Mapping.objects.all()
        if 'excelFile' in request.FILES:

            # retrieve POST request information
            uploaded_file = request.FILES['excelFile']
            try:
                selected_mapping_id = request.POST['mapping']
                selected_mapping = Mapping.objects.get(pk=selected_mapping_id)
                graph_name = selected_mapping.graph_name
                selected_mapping_title = selected_mapping.title
            except KeyError:
                return render(request, "app/upload.html", {"mappings": mappings, 'error': 'Please select a mapping'})

            # if valid file extension, upload file to knowledge base
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                file_name = uploaded_file.name
                df = pd.read_excel(uploaded_file)
                insert_pandas_dataframe_into_sparql_graph(graph_name, selected_mapping_title, df)
                return render(request, "app/upload.html", {"mappings": mappings, 'file_name': file_name})
            else:
                return render(request, "app/upload.html", {"mappings": mappings, 'error': 'Invalid file format: an .xls or .xlsx file is expected'})
        else:
            return render(request, "app/upload.html", {"mappings": mappings, 'error': 'No file uploaded'})
    elif request.method == 'GET':
        mappings = search_mappings(request)
        return render(request, "app/upload.html", {"mappings": mappings, 'error':None})
    else:
        return render(request, "app/upload.html", {"data": 'unresolved request'})

def download(request):
    """
    Download an excel sheet
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered download page.
    """

    # If user is accessing this page for the first time,
    # present the user with a list of mappings available.
    mappings = Mapping.objects.all()
    if request.method == 'GET':
        return render(request, "app/download.html", {"mappings": mappings})
    
    # If user has selected a mapping to download,
    # convert fuseki to excel and allow user to download file
    if request.method == 'POST':
        try:
            selected_mapping_id = request.POST['mapping']
            selected_mapping = Mapping.objects.get(pk=selected_mapping_id)

            # query fuseki with mapping to create dataframe
            relations, graph_name = selected_mapping.fuseki_relations, selected_mapping.graph_name
            fuseki_response = fuseki_relations_to_sparql_response(relations, graph_name)
            headers, df = fuseki_response_to_DataFrame(fuseki_response)

            # convert dataframe to excel in memory
            file_name='excel_data.xlsx'
            in_memory_file = BytesIO()
            df.to_excel(in_memory_file, index=False)
            in_memory_file.seek(0, 0)
            excel_file_obj = File(in_memory_file,  name=file_name)

            # save excel in memory to GeneratedExcelFile obj in Django
            file_model = GeneratedExcelFile(excel_file=excel_file_obj)
            file_model.save()

            return render(request, "app/export-success.html", {'file_pk': file_model.pk, 'selected_mapping': selected_mapping, 'df':df, 'headers':headers})
        except KeyError:
                return render(request, "app/download.html", {"mappings": mappings, 'error': 'Please select a mapping'})

def download_file(request, pk):
    """
    Download a preexisting excel file
    
    :param request: The request object.
    :type request: HttpRequest
    :param pk: The primary key of the excel file to download.
    :type pk: int
    :return: The rendered download page.
    """
    
    file_model = GeneratedExcelFile.objects.get(pk=pk)
    file_name = file_model.excel_file.name.split('/')[-1]
    response = HttpResponse(file_model.excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

def register(request):
    """
    Register a new user
    
    :param request: The request object.
    :type request: HttpRequest
    :return: The rendered register page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
