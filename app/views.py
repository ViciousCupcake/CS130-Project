from django.shortcuts import render

from django.http import HttpResponse
from .models import Mapping
from .forms import MappingForm

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
