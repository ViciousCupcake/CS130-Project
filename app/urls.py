from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.list, name='list'),
    path("import/", views.import_mapping, name="import"),
    path("accounts/", include("django.contrib.auth.urls")),
]
