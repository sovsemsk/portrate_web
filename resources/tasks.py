import asyncio
from celery import shared_task
from django.conf import settings
from telegram import Bot

from parsers.yandex.utils import YandexParser

@shared_task
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))


@shared_task
def selenium_task():
    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int('112689815427'))
    o = parser.parse(type_parse='company')
    print(o)