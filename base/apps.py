from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"
    verbose_name = "Base Models"

    def ready(self):
        import base.signals
