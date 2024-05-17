from django.apps import AppConfig
from django.core.management import call_command


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    def ready(self):
        call_command('send_mail')