import asyncio
from celery import shared_task
from django.conf import settings
from telegram import Bot

@shared_task
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))
