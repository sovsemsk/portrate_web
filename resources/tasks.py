import asyncio

from celery import shared_task
from django.conf import settings
from telegram import Bot

from parsers.gis import GisParser
from parsers.yandex import YandexParser
from resources.models import Company


@shared_task(name="Отправка сообщения Telegram")
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))
    return f"Done send to {telegram_id}"


@shared_task(name="Парсинг карточек")
def parse_cards(company_id):
    result = []

    company_with_yandex_link = Company.objects.filter(
        is_active=True,
        is_yandex_reviews_download=True
    ).exclude(
        yandex_parser_link=None,
    ).exclude(
        yandex_parser_link="",
    ).values("id").first()

    if company_with_yandex_link:
        yandex_parser = YandexParser(company_id)
        yandex_result = yandex_parser.parse()
        result.append(yandex_result)
    else:
        result.append("Company not valid for YandexParser")

    company_with_gis_link = Company.objects.filter(
        is_active=True,
        is_gis_reviews_download=True
    ).exclude(
        gis_parser_link=None
    ).exclude(
        gis_parser_link="",
    ).values("id").first()

    if company_with_gis_link:
        gis_parser = GisParser(company_id)
        gis_result = gis_parser.parse()
        result.append(gis_result)
    else:
        result.append("Company not valid for GisParser")

    return f"Done for company [{company_id}] with result [{', '.join(result)}]"
