import json
import re

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from telegram import Bot, Update, MessageEntity

from resources.models import Profile
from resources.tasks import send_telegram_text_task


@csrf_exempt
@require_http_methods(["POST"])
def telegram_update(request):
    # @TODO: Добавить авторизацию и проверку запроса от api, это важно
    bot = Bot(settings.TELEGRAM_BOT_API_SECRET)
    update = Update.de_json(json.loads(request.body), bot)
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
        telegram_update_start(message=message)

    return HttpResponse()


def telegram_update_start(message):
    profile = Profile.objects.filter(api_secret=message.text.replace("/start ", "")).first()

    if not profile:
        return

    try:
        profile.telegram_id = message.from_user.id
        profile.save()
        send_telegram_text_task.delay(message.from_user.id, "🍾 Вы подписаны на уведомления telegram")

    finally:
        return
