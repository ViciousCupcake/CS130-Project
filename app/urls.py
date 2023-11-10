from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.list, name='list'),

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
    path("select/", views.select_mapping, name="select"),
    path("modify/", views.modify_mapping, name="modify"),
    path("modify/<int:pk>/", views.modify_mapping, name="modify"),
    path("delete/", views.delete_mapping, name="delete"),
]
