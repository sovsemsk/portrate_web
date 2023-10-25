from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from .forms import LoginForm


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.add_message(
                request,
                messages.ERROR,
                'Заполните все поля формы'
            )

            return render(request, 'extensions/login.html', {'form': form})

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if not user:
            messages.add_message(
                request,
                messages.ERROR,
                'Пользователь не найден'
            )
            return render(request, 'extensions/login.html', {'form': form})

        if not user.is_active:
            messages.add_message(
                request,
                messages.ERROR,
                'Пользователь не активен'
            )
            return render(request, 'extensions/login.html', {'form': form})

        auth_login(request, user)
        return redirect('dashboard_index')

    else:
        form = LoginForm(request.POST)
        return render(request, 'extensions/login.html', {'form': form})
