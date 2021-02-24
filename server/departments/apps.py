from django.apps import AppConfig


class DepartmentsConfig(AppConfig):
    name = 'departments'

    def ready(self):
        import departments.signals