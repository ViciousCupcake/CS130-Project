from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.list, name='list'),
    path("import/", views.import_mapping, name="import"),
    path("upload/", views.upload, name="upload"),
]
