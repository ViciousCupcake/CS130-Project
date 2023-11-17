from django.contrib import admin
from app.models import Mapping, GeneratedExcelFile


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'last_updated']

@admin.register(GeneratedExcelFile)
class GeneratedExcelFileAdmin(admin.ModelAdmin):
    list_display = ['excel_file', 'last_updated']
