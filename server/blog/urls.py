from django.urls import path
from .views import EditPostView, MainPage, image_upload

app_name = 'blog'

urlpatterns = [
    path("", MainPage.as_view(), name="main_page"),
    path("edit/", EditPostView.as_view(), name="edit_post"),
    path("upload_image/", image_upload, name="upload_image"),
]