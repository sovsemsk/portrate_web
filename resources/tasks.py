import asyncio

from celery import shared_task
from django.conf import settings
from telegram import Bot

from parsers.gis import GisParser
from parsers.yandex import YandexParser


@shared_task(name="Отправка сообщения Telegram")
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))
    return f"Done send to {telegram_id}"


@shared_task(name="Парсинг Яндекс Карты")
def parse_yandex(company_id):
    parser = YandexParser(company_id)
    result = parser.parse()
    return f"Done for company [{company_id}] with result [{result}]"


@shared_task(name="Парсинг 2Гис Карты")
def parse_gis(company_id):
    parser = GisParser(company_id)
    result = parser.parse()
    return f"Done for company [{company_id}] with result [{result}]"
