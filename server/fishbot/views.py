from django.http import JsonResponse
from .models import Subscribtion, UserAction, TelegramToken
import datetime
from django.utils import timezone

# Create your views here.


def user_action(request, token):
    sub = Subscribtion.objects.filter(token=token, active=True).first()
    if sub.start < timezone.now() < sub.end:
        pass
    else:
        user = sub
        user.active = False
        user.save()
        return JsonResponse(
            {"status": 0, "message": "Время подписки вышло"})
    ip = request.body.decode("utf-8")
    if sub:
        created_time = timezone.now() - datetime.timedelta(minutes=60)
        actions = UserAction.objects.filter(user=sub.user).order_by('-pk')
        if actions and actions[0].time > created_time:
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