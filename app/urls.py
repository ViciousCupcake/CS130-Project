"""
This module defines the urls for the app. The urls are as follows:
    - /: Index page
    - /list: Page that lists all mappings
    - /upload: Page enabling users to upload excel files
    - /download: Page enabling users to download excel files
    - /accounts/login: Login page
    - /accounts/logout: Logout page
    - /register: Page that allows users to register
    - /select: Page that allows users to select a mapping to modify
    - /modify: Page that allows users to create a mapping
    - /modify/<int:pk>: Page that allows users to modify a preexisting mapping
    - /delete: API endpoint that allows users to delete a mapping. This page cannot be accessed directly.
    - /visualize: Page that allows users to visualize a mapping
    - /download/<int:pk>: API endpoint that allows users to download a preexisting excel file
"""

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
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'), 

    # CRUD Operations that administrative users can perform.
    # Login is required to access these pages.
    path("select/", views.select_mapping, name="select"), # Page that allows users to select a mapping to modify
    path("modify/", views.modify_mapping, name="modify"), # Page that allows users to create a mapping
    path("modify/<int:pk>/", views.modify_mapping, name="modify"), # Page that allows users to modify a preexisting mapping
    path("delete/", views.delete_mapping, name="delete"), # API endpoint that allows users to delete a mapping. This page cannot be accessed directly.
    path("visualize/", views.visualize_mapping, name='visualize_mapping'),

    # API endpoints that allow users to download excel files
    path("download/<int:pk>/", views.download_file, name="download_file"), # API endpoint that allows users to download a preexisting excel file
]
