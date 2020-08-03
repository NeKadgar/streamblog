from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from members.session_profile import SessionProfile
from django.http import JsonResponse
from blog.models import Post, Image
from blog.forms import ImageForm
from .utils import convert_editorjs_to_html
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
        print(data["content"])
        html = convert_editorjs_to_html(data["content"]["blocks"])
        print(html)
        post = Post(title=data["title"], content=data["content"], author=request.user)
        # post.save()
        return render(request, "blog/edit.html")

def image_upload(request, *args, **kwargs):
    print(request.FILES)
    if request.method == "POST" and request.FILES["image"]:
        image = Image(author=request.user, image=request.FILES["image"])
        image.save()
    return JsonResponse({
        "success": 1,
        "file": {
            "url": image.image.url,
        }
    })
