from django.http import HttpResponse
from django.shortcuts import render, redirect
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
        if "final_save" in request.POST:
            id = request.POST.get("post_id", None)
            title = request.POST.get("title", None)
            description = request.POST.get("description", None)
            tags = request.POST.get("tags", None)
            if id and title and description and tags:
                print(312)
                post = get_object_or_404(Post, id=id, author=request.user)
                post.title = title
                post.description = description
                for tag in tags.split(","):
                    post.tags.add(tag)
                post.save()
            return redirect("/")
        else:
            data = json.loads(request.POST["json"])
            post = Post(title=data["title"], content=data["content"], author=request.user)
            post.save()
            desc, image = get_presave_info(post.content)
            return render(request, "blog/save-post.html", {"title": post.title, "post_id": post.id})


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
