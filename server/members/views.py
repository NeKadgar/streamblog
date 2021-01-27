from django.core.validators import validate_image_file_extension
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout
from members.models import Profile, UserLink
from django.shortcuts import get_object_or_404
from blog.models import Post
from django.contrib.auth.decorators import login_required
from members.utils import get_followers_count, is_following, is_email_correct, is_image_correct
from django.http import JsonResponse
from members.session_profile import SessionProfile


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if kwargs:
            return render(request, "members/login.html", {"sign_up": True})
        return render(request, "members/login.html", {"error": ""})

    def post(self, request, *args, **kwargs):  # регистрация не доделана
        if "sign-up" in request.POST:
            username = request.POST.get("name", None)
            email = request.POST.get("email", None)
            password = request.POST.get("password", None)
            if username and email and password:
                if User.objects.filter(username=username):
                    return render(request, "members/login.html",
                                  {"error_signup": "Имя уже занято другим пользователем"})
                if User.objects.filter(email=email):
                    return render(request, "members/login.html",
                                  {"error_signup": "Email уже привязан к другому аккаунту"})
                if len(password) > 7 and password == request.POST.get("confirm_password", None):
                    User.objects.create_user(username=username, password=password, email=email)
                    user = authenticate(username=email, password=password)
                    login(request, user)
                    return redirect("blog:main_page")
                return render(request, "members/login.html", {"error_signup": "Пароль должен быть длиной 8+ символов"})
            return render(request, "members/login.html", {"error_signup": "Проверьте введенные данные"})

        if "sign-in" in request.POST:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
            else:
                return render(request, "members/login.html", {"error": "Проверьте введеные данные"})
        return redirect("blog:main_page")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("blog:main_page")


class ProfileView(View):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        followers = get_followers_count(user)
        posts = Post.objects.filter(author=user).order_by('-created')
        popular_posts = Post.objects.filter(author=user).order_by('-post_views')[:5]
        profile = get_object_or_404(Profile, user=user)

        if request.user.is_anonymous:
            is_follower = False
        else:
            is_follower = user.follower_links.filter(from_user=request.user).exists()
        SessionProfile(request).add_profile(profile.id)
        return render(request, "members/profile.html",
                      {"profile": profile, "posts": posts, "followers": followers, "is_follower": is_follower,
                       "popular_posts": popular_posts})

    def post(self, request):
        if "edit_profile" in request.POST:
            profile = get_object_or_404(Profile, user=request.user)
            email = request.POST.get("email", None)
            username = request.POST.get("username", None)
            fname = request.POST.get("fname", None)
            lname = request.POST.get("lname", None)
            profile_name = request.POST.get("profile_name", None)
            bio = request.POST.get("bio", None)
            photo = request.FILES.get("photo", None)
            banner = request.FILES.get("banner", None)
            if is_email_correct(email):
                request.user.email = email
            if username and not User.objects.filter(username=username).exists():
                request.user.username = username
            if len(fname) < 100:
                request.user.first_name = fname
            if len(lname) < 100:
                request.user.last_name = lname
            if profile_name == Profile.FULLNAME and len(fname) > 0:
                profile.profile_name = Profile.FULLNAME
            else:
                profile.profile_name = Profile.USERNAME
            if len(bio) <= 2000:
                profile.bio = bio
            if is_image_correct(photo):
                profile.photo = photo
            if is_image_correct(banner):
                profile.banner = banner

            request.user.save()
            profile.save()
            return redirect("members:profile")


        profile = get_object_or_404(Profile, user=request.user)
        return render(request, "members/edit-profile.html", {"profile": profile})


@login_required
def follow(request, username):
    """
    Adds a "following" edge from the authenticated user to the user specified
    by the username in the URL.
    """
    if request.user.is_anonymous():
        return redirect("members:login")
    user = get_object_or_404(User, username=username)
    ul, created = UserLink.objects.get_or_create(from_user=request.user,
                                                 to_user=user)
    # return redirect("members:profile", username=user.username)
    return JsonResponse({"status": 1})


@login_required
def unfollow(request, username):
    """
    Removes a "following" edge from the authenticated user to the user
    specified by the username in the URL.

    """
    user = get_object_or_404(User, username=username)
    try:
        ul = UserLink.objects.get(from_user=request.user, to_user=user)
        ul.delete()
        deleted = True
    except UserLink.DoesNotExist:
        deleted = False
    # return redirect("members:profile", username=user.username)
    return JsonResponse({"status": 1})
