from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.index, name="index"), # Index page
    path("list/", views.list, name='list'), # Page that lists all mappings
    path("upload/", views.upload, name="upload"), # Page enabling users to upload excel files
    path("download/", views.download, name="download"), # Page enabling users to download excel files

    # This defines:
        # accounts/login/ [name='login']
        # accounts/logout/ [name='logout']
    # These paths are yet unimplemented:
        # accounts/password_change/ [name='password_change']
        # accounts/password_change/done/ [name='password_change_done']
        # accounts/password_reset/ [name='password_reset']
        # accounts/password_reset/done/ [name='password_reset_done']
        # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
        # accounts/reset/done/ [name='password_reset_complete']
    path("accounts/", include("django.contrib.auth.urls")),

    # CRUD Operations that administrative users can perform.
    # Login is required to access these pages.
    path("select/", views.select_mapping, name="select"), # Page that allows users to select a mapping to modify
    path("modify/", views.modify_mapping, name="modify"), # Page that allows users to create a mapping
    path("modify/<int:pk>/", views.modify_mapping, name="modify"), # Page that allows users to modify a preexisting mapping
    path("delete/", views.delete_mapping, name="delete"), # API endpoint that allows users to delete a mapping. This page cannot be accessed directly.

    # API endpoints that allow users to download excel files
    path("download/<int:pk>/", views.download_file, name="download_file"), # API endpoint that allows users to download a preexisting excel file
]
