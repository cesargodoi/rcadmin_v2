from django.apps import AppConfig


class PublicworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.publicwork"

    def ready(self):
        import apps.publicwork.signals  # noqa
