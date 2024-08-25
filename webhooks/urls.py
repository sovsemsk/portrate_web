from django.urls import path

from .views import tbank_update, telegram_update

urlpatterns = [
    path("telegram_update", telegram_update, name="telegram_update"),
    path("tbank_update", tbank_update, name="tbank_update")
]
