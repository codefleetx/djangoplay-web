from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locations'

    def ready(self):
        """Connect signals for the locations app."""
        pass
        # import locations.signals  # Import signals to ensure they are connected
