import asyncio
from celery import shared_task
from django.conf import settings
from telegram import Bot
from resources.models import NegativeMessage


@shared_task
def telegram_notify_subscribed(telegram_id):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(
        telegram_id, 'Вы подписаны на уведомления'
    ))


@shared_task
def telegram_notify_negative_message(telegram_id, negative_message_id):
    negative_message = NegativeMessage.objects.get(id=negative_message_id)

    tags = ', '.join(
        list(
            negative_message.negative_message_tag.values_list('text', flat=True)
        )
    )

    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id,
f'''📍 Негативное сообщение в Портрете.

🏪 Филиал:
{negative_message.branch}

📯 Теги:
{tags[:len(tags) - 2]}

📱 Телефон:
{negative_message.phone}

📜 Комментарий:
{negative_message.text}'''
        ))

