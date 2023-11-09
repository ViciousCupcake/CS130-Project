from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Mapping
from .forms import MappingForm
import pandas as pd
from django.http import HttpResponse

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

@login_required
def export_mapping(request, pk=None):
    """View that allows Administrative users to export a mapping into excel file and view it"""

    # fetch the selected mapping
    try:
        mapping = Mapping.objects.get(pk=pk)
    except Mapping.DoesNotExist:
        return render(request, "app/export.html", {'mapping': None, 'data' : None})

    # TODO: create dataframe from querying fuseki using the mapping to display in preview

    # transform fuseki response into a pandas DataFrame
    data = {
        "X": [1,2,3,4, 5, 6, 7, 8, 9, 10],
        "Y":[5,6,7, 8, 9, 10, 11, 12, 13, 14]
    }
    headers = data.keys()
    df = pd.DataFrame(data)

    # track the serialized data to download in a session variable
    request.session["data_to_download"] = df.to_json()

    return render(request, "app/export.html", {'mapping': mapping, 'headers': headers, "df":df})

@login_required
def download_excel(request):
    """View that allows Administrative users to export a mapping into excel file and download it"""

    # If user wants to export excel, return the excel as a response
    if request.method == "POST":
        df = pd.read_json(request.session["data_to_download"])
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="excel_data.xlsx"'

        with pd.ExcelWriter(response) as writer:
            df.to_excel(writer, index=False)

        return response
