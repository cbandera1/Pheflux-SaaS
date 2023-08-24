from django.apps import AppConfig
from django.apps import AppConfig


class PhefluxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Pheflux'

    def ready(self):
        import Pheflux.signals  # Reemplaza "your_app" con el nombre de tu aplicación
