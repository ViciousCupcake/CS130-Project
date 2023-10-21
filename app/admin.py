from django.contrib import admin
from app.models import Mapping


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'last_updated']
