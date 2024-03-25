from django.urls import path

from .views import telegram_update

urlpatterns = [
    path("telegram_update", telegram_update, name="telegram_update")
]
