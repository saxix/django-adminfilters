from django.apps import AppConfig


class Config(AppConfig):
    name = "adminfilters"

    def ready(self) -> None:  # noqa: PLR6301
        from . import checks  # noqa: F401, PLC0415
