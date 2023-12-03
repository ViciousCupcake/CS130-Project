"""
URL configuration for cs130_efi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
This module defines the following URLs:
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
from django.contrib import admin
from django.urls import include, path

# Root URL configuration
urlpatterns = [
    path('doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
