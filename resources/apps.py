"""
App configuration for the resources app.
"""

from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    """Configuration for the resources app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resources'
    verbose_name = 'Resources'
    
    def ready(self):
        """Called when the app is ready."""
        # Import signals if any
        pass
