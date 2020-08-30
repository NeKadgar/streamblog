from django.contrib import admin
from .models import Subscribtion, UserAction, TelegramToken

# Register your models here.

admin.site.register(Subscribtion)
admin.site.register(UserAction)
admin.site.register(TelegramToken)