from django.urls import path
from . import views

urlpatterns = [
    path(
        'telegram_update',
        views.webhooks_telegram_update,
        name='webhooks_telegram_update'
    )
]
