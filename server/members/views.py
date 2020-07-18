from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout

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
            print("qwe")
            if user:
                login(request, user)
            else:
                return render(request, "members/login.html", {"error": "Проверьте введеные данные"})
        return redirect("blog:main_page")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("blog:main_page")
