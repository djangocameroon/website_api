from django.apps import AppConfig

class EventsConfig(AppConfig):
    name = 'apps.events'

    def ready(self):
        import apps.events.signals