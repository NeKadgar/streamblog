from django.contrib.auth.models import User
from django.http import HttpResponse, RawPostDataException
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from members.session_profile import SessionProfile
from django.http import JsonResponse
from blog.models import Post, Image, PostViews, BaseImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import MyForm
from .utils import convert_editorjs_to_html, get_presave_info, get_tags
import json
from members.models import Profile
from taggit.models import Tag
from django.utils.safestring import SafeString
import datetime
from members.utils import is_image_correct
# Create your views here.

class MainPage(View):
    def get(self, request):
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)
        from_date = datetime.datetime.now() - datetime.timedelta(days=7)

        trends_posts = Post.objects.filter(created__range=[from_date, datetime.datetime.now()]).order_by("-post_views")[:8]
        tags = Post.tags.most_common()[:8]
        recommend_posts = SessionProfile(request).get_recommendations()
        recent_posts = Post.objects.all().order_by("-created")

        paginator = Paginator(recent_posts, 15)
        page = request.GET.get('page')
        try:
            recent_posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            recent_posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            recent_posts = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, "blog/recent-list.html", {"recent_posts": recent_posts})
        return render(request, "blog/main.html", {"tags": tags, "recommend_posts": recommend_posts, "recent_posts": recent_posts, "trends_posts": trends_posts})


class EditPostView(View):
    def get(self, request, slug=None):
        if not request.user.is_anonymous:
            if slug:
                post = get_object_or_404(Post, slug=slug)
                if post.author == request.user:
                    return render(request, "blog/edit.html", {"post": post, "content": json.dumps(post.content)})
                else:
                    return redirect("/")
            return render(request, "blog/edit.html")
        else:
            return redirect("members:login")

    def post(self, request, slug=None):
        if "final_save" in request.POST:
            id = request.POST.get("post_id", None)
            title = request.POST.get("title", None)
            description = request.POST.get("description", None)
            tags = request.POST.get("tags", None)
            image = request.FILES.get('image', False)
            bad_chars = [' , ', ' ,', ', ']
            if id and title and description and tags:
                post = get_object_or_404(Post, id=id, author=request.user)
                post.title = title
                post.description = description
                post.status = Post.PUBLISHED
                if image:
                    post.preview_image = image
                for i in bad_chars:
                    tags = tags.replace(i, ",")
                for tag in tags.split(","):
                    if len(tag) > 1:
                        post.tags.add(tag)
                post.save()
                return redirect("blog:post", post_slug=post.slug)
            return redirect("/")
        else:
            data = json.loads(request.POST["json"])
            if data["title"] != "" and data["content"]["blocks"] != "":
                if slug:
                    post = get_object_or_404(Post, slug=slug, author=request.user)
                    post.title = data["title"]
                    post.content = data["content"]
                else:
                    post = Post(title=data["title"], content=data["content"], author=request.user)
                post.save()
                desc, image = post.description, post.preview_image
                return render(request, "blog/save-post.html",
                              {"title": post.title, "post_id": post.id, "post_desc": desc, "post_preview": image,
                               "post_tags": post.tags})


def create_post(request):
    pass


class PostView(View):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        html = convert_editorjs_to_html(post.content)
        author = get_object_or_404(Profile, user=post.author)
        if request.user.is_anonymous:
            is_follower = False
        else:
            is_follower = author.user.follower_links.filter(from_user=request.user).exists()
            PostViews.objects.get_or_create(post=post, user=request.user)
        SessionProfile(request).add_post(post.id)
        return render(request, "blog/post.html", {"post": post, "content": html, "author": author, "is_follower": is_follower})


class TagSortView(View):
    def get(self, request, tag):
        tags = Tag.objects.filter(name=tag).values_list('name', flat=True)
        posts = Post.objects.filter(tags__name__in=tags)
        popular_posts = Post.objects.filter(tags__name__in=tags).order_by('-post_views')[:5]
        return render(request, "blog/posts_list.html", {"posts": posts, "tag": tag, "popular_posts": popular_posts})


def image_upload(request, *args, **kwargs):
    try:
        data = json.loads(request.body)
    except RawPostDataException:
        data = {}
    image = request.FILES.get("image", None)
    image_url = data.get("image_url", None)
    url = ""
    if request.method == "POST":
        if image and is_image_correct(image):
            image = Image(author=request.user, image=request.FILES["image"])
            image.save()
            url = image.image.url
        elif image_url:
            url = image_url
    return JsonResponse({
        "success": 1 if url else 0,
        "file": {
            "url": url,
        }
    })

def base_image(request, name=None):
    try:
        image = BaseImage.objects.get(name=name)
    except:
        pass
    else:
        print(image.image.url)
        return image.image.url