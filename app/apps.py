"""
This module defines the configuration for the app. Specifically, it defines the field used for the primary key for all models in the app. This module is important because it allows us to use a custom primary key for all models in the app.
"""


from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    This class defines the configuration for the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
