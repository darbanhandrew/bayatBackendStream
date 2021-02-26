from django.apps import AppConfig


class OnetimeConfig(AppConfig):
    name = 'oneTime'

    def ready(self):
        import oneTime.signals

