from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from SPARQLWrapper import SPARQLWrapper, POST
from .models import Mapping
from .forms import MappingForm
from .utils.parse_helpers import parse_excel

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


def upload_to_fuseki(rdf_data):
    """Uploaded parsed data (rdf data) to fuseki"""

    sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/update")
    # Set the credentials for authentication
    username = "admin"
    password = "postgres"
    sparql.setCredentials(username, password)
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
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                file_name = uploaded_file.name
                rdf_data = parse_excel(uploaded_file, file_name)
                upload_to_fuseki(rdf_data)
                return render(request, "app/upload_success.html", {'file_name': file_name})
            else:
                return render(request, "app/upload.html", {'error': 'Invalid file format'})
        else:
            return render(request, "app/upload.html", {'error': 'No file uploaded'})

    return render(request, "app/upload.html", {'data': 'Hello, world!'})
