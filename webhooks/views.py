import json
import re

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from telegram import Update, MessageEntity

from extensions.models import Profile


# Вебхук для telegram
@csrf_exempt
@require_http_methods(['POST'])
def webhooks_telegram_update(request):
    # @TODO: Добавить авторизацию и проверку запроса от api, это важно
    update = Update.de_json(json.loads(request.body), settings.TELEGRAM_BOT)
    message = update.message or update.edited_message

    # Сброс если не команда бота
    if not message:
        return HttpResponse()

    if not message.entities:
        return HttpResponse()

    if not message.entities[0].type == MessageEntity.BOT_COMMAND:
        return HttpResponse()

    # Хендлер команды /start Y1GNT1F5
    if re.match(r"/start ([a-z,A-Z,0-9]){8}", message.text):
        return webhooks_telegram_update_start(message=message)

    # Хендлер команды /stop Y1GNT1F5
    if re.match(r"/stop ([a-z,A-Z,0-9]){8}", message.text):
        return webhooks_telegram_update_stop(message=message)


# Хендлер команды /start Y1GNT1F5
def webhooks_telegram_update_start(message):
    # Получение пользователя
    profile = Profile.objects.filter(
        api_secret=message.text.replace('/start ', '')
    ).first()

    # Сброс если нет такого пользователя
    if not profile:
        return HttpResponse()

    # Создание подписки
    try:
        profile.telegram_id = message.from_user.id
        profile.save()

    finally:
        return HttpResponse()


# Хендлер команды /stop Y1GNT1F5
def webhooks_telegram_update_stop(message):
    pass
