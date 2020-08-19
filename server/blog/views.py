from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from members.session_profile import SessionProfile
from django.http import JsonResponse
from blog.models import Post, Image
from blog.forms import MyForm
from .utils import convert_editorjs_to_html, get_presave_info
import json

# Create your views here.

class MainPage(View):
    def get(self, request):
        print(SessionProfile(request).show())
        return render(request, "blog/main.html")


class EditPostView(View):
    def get(self, request):
        return render(request, "blog/edit.html")

    def post(self, request):
        data = json.loads(request.POST["json"])
        post = Post(title=data["title"], content=data["content"], author=request.user)
        # post.save()
        desc, image = get_presave_info(post.content)
        return render(request, "blog/save-post.html", {"title": post.title})


def create_post(request):
    pass


class PostView(View):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        html = convert_editorjs_to_html(post.content)
        post.tags.add("programming", "developer")
        print(post.tags.all())
        return render(request, "blog/post.html", {"title": post.title, "content": html})


def image_upload(request, *args, **kwargs):
    if request.method == "POST" and request.FILES["image"]:
        image = Image(author=request.user, image=request.FILES["image"])
        image.save()
    return JsonResponse({
        "success": 1,
        "file": {
            "url": image.image.url,
        }
    })
