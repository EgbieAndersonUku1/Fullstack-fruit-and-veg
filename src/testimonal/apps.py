from django.apps import AppConfig


class TestimonalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testimonal'
    
    def ready(self) -> None:
        import testimonal.signals
