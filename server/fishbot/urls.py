from django.urls import path
from .views import user_action, get_telegram_token, check_status

urlpatterns = [
    path("telegram_token/", get_telegram_token),
    path("<slug:token>/", user_action),
    path("check/<slug:token>/", check_status),
]