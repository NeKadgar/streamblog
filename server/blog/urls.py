from django.urls import path
from .views import EditPostView, MainPage, PostView, image_upload, TagSortView, base_image

app_name = 'blog'

urlpatterns = [
    path("", MainPage.as_view(), name="main_page"),
    path("articles/<slug:post_slug>/", PostView.as_view(), name="post"),
    path("create/", EditPostView.as_view(), name="create_post"),
    path("edit/<slug:slug>", EditPostView.as_view(), name="edit_post"),
    path("tag/<str:tag>", TagSortView.as_view(), name="tag_view"),
    path("upload_image/", image_upload, name="upload_image"),
    path("base_image/<str:name>", base_image, name="base_image"),
]