from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from members.session_profile import SessionProfile

# Create your views here.

class MainPage(View):
    def get(self, request):
        print(SessionProfile(request).show())
        return render(request, "blog/main.html")


class EditPostView(View):
    def get(self, request):
        return render(request, "blog/edit.html")

    def post(self, request):
        print(request.POST)

def image_upload(request, *args, **kwargs):
    print(request)
    return HttpResponse("123")