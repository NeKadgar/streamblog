from django.contrib import admin
from .models import Post, Image, PostViews, BaseImage

# Register your models here.

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(PostViews)
admin.site.register(BaseImage)
