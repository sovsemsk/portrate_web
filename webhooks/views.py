import asyncio
import json
import re
from datetime import datetime, timezone

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from djmoney.money import Money
from telegram import Bot, Update, MessageEntity

from billing.tbank import Tbank
from resources.models import Profile, Payment


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

    profile.telegram_id = message.from_user.id
    profile.save()
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(message.from_user.id, "🍾 Вы подписаны на уведомления telegram"))


@csrf_exempt
@require_http_methods(["POST"])
def tbank_update(request):
    data = json.loads(request.body)

    if data.get("Success") and data.get("Status") == "CONFIRMED":
        # Проверка обновления
        token = data.get("Token")
        data["Success"] = str(data.get("Success")).lower()
        data.pop("Token")

        if Tbank().create_hash(data) == token:
            # Обновление платежа
            payment = Payment.objects.get(api_secret=data.get("OrderId"))
            payment.is_paid = True
            payment.paid_at = datetime.now(timezone.utc)
            payment.card_id = data.get("CardId")
            payment.save()

            # Обновление профиля
            payment.user.profile.balance = Money(payment.user.profile.balance.amount + payment.amount.amount, "RUB")
            payment.user.save()

    return HttpResponse()
