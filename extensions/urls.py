from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='extensions_login'),
    path('profile/', views.profile, name='extensions_profile'),
    path('telegram_notify_unsubscribe/', views.telegram_notify_unsubscribe, name='extensions_telegram_notify_unsubscribe'),
]
