from django.urls import path
from .views import LoginView, LogoutView

app_name = "members"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/<str:reg>", LoginView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
