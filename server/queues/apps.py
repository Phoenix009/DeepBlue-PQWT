from django.apps import AppConfig


class QueuesConfig(AppConfig):
    name = 'queues'

    def ready(self):
        import queues.signals
