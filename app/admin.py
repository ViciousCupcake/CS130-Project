"""
This module defines the admin interface for the app. Specifically, it defines
the admin interface for the Mapping and GeneratedExcelFile models. This module
is important because it allows us to view the contents of the database in a
user-friendly way. It also allows us to add, edit, and delete database entries
without the need to write SQL queries.

"""


from django.contrib import admin
from app.models import Mapping, GeneratedExcelFile


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    """
    This class defines the admin interface for the :model: `app.Mapping` model.

    This defines what properties are displayed in the admin interface.
    """
    list_display = ['title', 'description', 'last_updated']

@admin.register(GeneratedExcelFile)
class GeneratedExcelFileAdmin(admin.ModelAdmin):
    """
    This class defines the admin interface for the :model: `app.GeneratedExcelFile` model.

    This defines what properties are displayed in the admin interface.
    """

    list_display = ['excel_file', 'last_updated']
