from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from members.session_profile import SessionProfile
from blog.models import Post
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
        post.save()
        return render(request, "blog/edit.html")

def image_upload(request, *args, **kwargs):
    print(request)
    return HttpResponse("123")