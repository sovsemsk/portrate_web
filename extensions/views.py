from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from resources.tasks import send_telegram_text_task
from .forms import LoginForm


@require_http_methods(("GET", "POST",))
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.add_message(
                request,
                messages.ERROR,
                "Заполните все поля формы"
            )

            return render(request, "extensions/login.html", {"form": form})

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        if not user:
            messages.add_message(
                request,
                messages.ERROR,
                "Пользователь не найден"
            )
            return render(request, "extensions/login.html", {"form": form})

        if not user.is_active:
            messages.add_message(
                request,
                messages.ERROR,
                "Пользователь не активен"
            )
            return render(request, "extensions/login.html", {"form": form})

        auth_login(request, user)
        return redirect("company_list")

    else:
        form = LoginForm(request.POST)
        return render(request, "extensions/login.html", {"form": form})


@require_http_methods(("GET", "POST",))
def logout(request):
    auth_logout(request)
    return redirect("extensions_login")


@login_required
@require_http_methods(("GET",))
def profile(request):
    return render(request, "extensions/profile.html", {
        "nav": "profile"
    })


@login_required
@require_http_methods(("GET",))
def telegram_notify_unsubscribe(request):
    send_telegram_text_task(request.user.profile.telegram_id, "👋🏼 Вы отписаны от уведомлений telegram")
    request.user.profile.telegram_id = None
    request.user.profile.save()

    return redirect(request.GET.get("next"))
