from django.apps import AppConfig


class Config(AppConfig):
    name = "adminfilters"

    def ready(self):
        from . import checks  # noqa
