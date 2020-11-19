from django.contrib import admin
from .models import Classifier


# Register your models here.

@admin.register(Classifier)
class ProfileAdmin(admin.ModelAdmin):
    pass