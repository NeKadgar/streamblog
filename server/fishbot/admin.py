from django.contrib import admin
from .models import Subscribtion, UserAction, TelegramToken

# Register your models here.

admin.site.register(TelegramToken)

@admin.register(Subscribtion)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'end', 'active')


@admin.register(UserAction)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'ip')
    fields = ('user', 'time', 'ip')
    list_filter = ('user',)
    readonly_fields = ['time']
