from django.http import JsonResponse
from .models import Subscribtion, UserAction, TelegramToken
from django.utils import timezone
import datetime

# Create your views here.


def user_action(request, token):
    sub = Subscribtion.objects.filter(token=token, active=True).first()
    ip = request.body.decode("utf-8")
    if sub:
        created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        actions = UserAction.objects.filter(user=sub.user, time__lte=created_time).order_by('-pk')
        print(actions)
        if actions:
            last_action = actions[0]
            if last_action.ip == ip:
                UserAction(user=sub.user, ip=ip).save()
                return JsonResponse({"status": 1, "message": "OK"})
            else:
                user = sub
                user.active = False
                user.save()
                return JsonResponse(
                    {"status": 0, "message": "Аккаунт заморожен из-за использования на нескольких устройствах"})
        UserAction(user=sub.user, ip=ip).save()
        return JsonResponse({"status": 1, "message": "OK"})
    return JsonResponse({"status": 0, "message": "Токен введен неверно или аккаунт заморожен"})


def get_telegram_token(request):
    token = TelegramToken.objects.latest("id")
    return JsonResponse({"token": str(token.token)})