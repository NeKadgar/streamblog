from django.http import JsonResponse
from .models import Subscribtion, UserAction, TelegramToken
import datetime
from django.utils import timezone
import requests
# Create your views here.

def check_status(request, token):
    subscibtion = Subscribtion.objects.filter(token=token).first()
    if subscibtion:
        if subscibtion.start < timezone.now() < subscibtion.end:
            pass
        else:
            subscibtion.active = False
            subscibtion.save()
        return JsonResponse(
            {"sub_status": subscibtion.active, "message": "OK", "sub_time": subscibtion.end.strftime('%d.%m.%Y %H:%M')})
    else:
        return JsonResponse(
            {"sub_status": False, "message": "Incorrect token", "sub_time": "..."})

def send_telegram_message(bot_message):
    bot_token = "865299523:AAEwrvzTwgvebQzABuTT-D9T3i_JDRyg_fY"
    bot_chat_id = str(405089115)
    api_url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + str(bot_message)
    requests.get(api_url)

def user_action(request, token):
    sub = Subscribtion.objects.filter(token=token).first()
    if sub.start < timezone.now() < sub.end:
        pass
    else:
        user = sub
        user.active = False
        user.save()
        return JsonResponse(
            {"status": 0, "message": "Время подписки вышло"})
    body = request.body.decode("utf-8")
    ip = ""
    sub = Subscribtion.objects.filter(token=token, active=True).first()
    if sub:
        created_time = timezone.now() - datetime.timedelta(minutes=60)
        actions = UserAction.objects.filter(user=sub.user).order_by('-pk')
        if actions and actions[0].time > created_time:
            last_action = actions[0]
            if last_action.ip == ip:
                UserAction(user=sub.user, ip=ip).save()
                return JsonResponse({"status": 1, "message": "OK"})
            else:
                # user = sub
                # user.active = False
                # user.save()
                return JsonResponse(
                    {"status": 0, "message": "Аккаунт заморожен из-за использования на нескольких устройствах"})
        UserAction(user=sub.user, ip=ip).save()
        return JsonResponse({"status": 1, "message": "OK"})
    return JsonResponse({"status": 0, "message": "Токен введен неверно или аккаунт заморожен"})


def get_telegram_token(request):
    token = TelegramToken.objects.latest("id")
    return JsonResponse({"token": str(token.token)})
