from django.apps import AppConfig


class PointerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pointer"
    verbose_name = "Pointer Models"

    def ready(self):
        import pointer.signals
