import json
import re

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from telegram import Update, MessageEntity

from resources.models import Branch
from webhooks.models import TelegramSubscription


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
    # Получение филиала
    branch = Branch.objects.filter(
        api_secret=message.text.replace('/start ', '')
    ).first()

    # Сброс если нет такого филиала
    if not branch:
        return HttpResponse()

    # Создание подписки
    try:
        TelegramSubscription.objects.create(
            telegram_user_id=message.from_user.id,
            group=branch.group,
            branch=branch
        )

    finally:
        return HttpResponse()


# Хендлер команды /stop Y1GNT1F5
def webhooks_telegram_update_stop(message):
    pass
