from django.apps import AppConfig


class HasiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hasite"

    def ready(self):
        import hasite.signals