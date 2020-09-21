from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
tz = timezone.get_default_timezone()

# Create your models here.

class Subscribtion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} подписка до {} {}".format(self.user.username, self.end, "Активна" if self.active else "Заморожена")


class TelegramToken(models.Model):
    token = models.CharField(max_length=255)

class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return "{}------{}".format(self.user.username, self.time.astimezone(tz).strftime('%d.%m.%Y %H:%M'))