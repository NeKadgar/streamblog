from django.contrib import admin
from members.models import Profile, UserLink


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(UserLink)
