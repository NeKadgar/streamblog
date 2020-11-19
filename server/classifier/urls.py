from django.urls import path
from .views import send_classifier

urlpatterns = [
    path("download/", send_classifier),
]