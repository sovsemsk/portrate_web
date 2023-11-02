from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='extensions_login'),
    path('logout/', views.logout, name='extensions_logout'),
    path('profile/', views.profile, name='extensions_profile'),
    path('telegram_notify_unsubscribe/', views.telegram_notify_unsubscribe, name='extensions_telegram_notify_unsubscribe'),
]
