from django.contrib import admin
from .models import Message, Client, Newsletter, Logs

admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Newsletter)
admin.site.register(Logs)