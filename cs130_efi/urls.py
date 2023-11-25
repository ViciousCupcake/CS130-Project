"""
URL configuration for cs130_efi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
