from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["author"]