from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'Auth'

    def ready(self):
        import Auth.signals
