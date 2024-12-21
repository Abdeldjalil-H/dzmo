from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = "control"
    verbose_name = "التحكم"

    def ready(self):
        import control.signals  # noqa: F401
