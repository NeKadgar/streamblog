from django.urls import path
from .views import LoginView, LogoutView, ProfileView, follow, unfollow

app_name = "members"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/<str:reg>", LoginView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit/profile/", ProfileView.as_view(), name="profile"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<str:username>", ProfileView.as_view(), name="profile"),
    path("follow/<str:username>", follow, name="follow"),
    path("unfollow/<str:username>", unfollow, name="unfollow"),
]
