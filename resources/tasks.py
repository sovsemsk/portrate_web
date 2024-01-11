import asyncio
import hashlib
from datetime import datetime, timezone

from celery import shared_task
from django.conf import settings
from parsers.yandex.utils import YandexParser
from telegram import Bot

from resources.models import Company, Notification, Review


@shared_task(name="Отправка сообщения Telegram")
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))


@shared_task(name="Парсинг рейтинга Яндекс Карты")
def parse_yandex_rate(company_id):
    company = Company.objects.get(pk=company_id)
    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int(company.yandex_id), company.yandex_reviews_last_parse_at)
    result = parser.parse(type_parse="company")

    # Запись данных
    company.yandex_rate = result.get("company_info", None).get("rating")
    company.yandex_rate_stars = result.get("company_info", None).get("start")
    company.yandex_rate_count = result.get("company_info", None).get("count_rating")

    # Запись агрегаций
    company.yandex_rate_last_parse_at = datetime.now(timezone.utc)
    company.save()


@shared_task(name="Парсинг отзывов Яндекс Карты")
def parse_yandex_reviews(company_id):
    company = Company.objects.get(pk=company_id)
    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int(company.yandex_id), company.yandex_reviews_last_parse_at)
    result = parser.parse(type_parse="reviews")

    # Запись данных
    for parsed_review in result.get("company_reviews", []):
        id = hashlib.md5(f"{parsed_review.get('name')}{parsed_review.get('date')}".encode()).hexdigest()

        try:
            review = Review.objects.create(
                name=parsed_review.get("name"),
                text=parsed_review.get("text"),
                answer=parsed_review.get("answer"),
                rate=parsed_review.get("stars"),
                remote_id=id,
                avatar_url=parsed_review.get("icon_href"),
                created_at=datetime.fromtimestamp(parsed_review.get("date"), tz=timezone.utc),
                company=company,
            )

            if parsed_review.get("stars") <= 3:
                Notification.objects.create(
                    company=review.company,
                    review=review,
                    text=review.text,
                    initiator=Notification.Initiator.YANDEX_NEGATIVE_REVIEW,
                )
        except:
            pass

    # Запись агрегаций
    company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
    company.save()


@shared_task(name="Парсинг отзывов Гис Карты")
def parse_gis_reviews(company_id):
    company = Company.objects.get(pk=company_id)
    parser = GisParser(settings.SELENIUM_BOT_API_SECRET, int(company.gis_id), company.gis_reviews_last_parse_at)
    result = parser.parse(type_parse="reviews")

    # Запись данных
    for parsed_review in result.get("company_reviews", []):
        id = hashlib.md5(f"{parsed_review.get('name')}{parsed_review.get('date')}".encode()).hexdigest()

        try:
            review = Review.objects.create(
                name=parsed_review.get("name"),
                text=parsed_review.get("text"),
                answer=parsed_review.get("answer"),
                rate=parsed_review.get("stars"),
                remote_id=id,
                avatar_url=parsed_review.get("icon_href"),
                created_at=datetime.fromtimestamp(parsed_review.get("date"), tz=timezone.utc),
                company=company,
            )

            if parsed_review.get("stars") <= 3:
                Notification.objects.create(
                    company=review.company,
                    review=review,
                    text=review.text,
                    initiator=Notification.Initiator.GIS_NEGATIVE_REVIEW,
                )

        except:
            pass

    # Запись агрегаций
    company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
    company.save()
