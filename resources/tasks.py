import asyncio
import hashlib
from datetime import datetime, timezone
from celery import shared_task
from django.conf import settings


@shared_task
def send_telegram_text_task(telegram_id, text):
    from telegram import Bot
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))


@shared_task
def parse_yandex_rate(company_id):
    from parsers.yandex.utils import YandexParser
    from resources.models import Company

    company = Company.objects.get(pk=company_id)

    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int(company.yandex_id))
    result = parser.parse(type_parse='company')

    company.yandex_rate = result.get('company_info', None).get('rating')
    company.yandex_rate_stars = result.get('company_info', None).get('start')
    company.yandex_rate_count = result.get('company_info', None).get('count_rating')
    company.yandex_rate_last_parse_at = datetime.now(timezone.utc)
    company.save()


@shared_task
def parse_yandex_reviews(company_id):
    from parsers.yandex.utils import YandexParser
    from resources.models import Company, Notification, Review

    company = Company.objects.get(pk=company_id)

    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int(company.yandex_id))
    result = parser.parse(type_parse='reviews')

    for parsed_review in result.get('company_reviews', None):
        id = hashlib.md5(
            f"{review.get('name')}{review.get('date')}".encode()
        ).hexdigest()

        try:
            review = Review.objects.create(
                name=       parsed_review.get('name'),
                text=       parsed_review.get('text'),
                answer=     parsed_review.get('answer'),
                rate=       parsed_review.get('stars'),
                remote_id=  id,
                avatar_url= parsed_review.get('icon_href'),
                created_at= datetime.fromtimestamp(parsed_review.get('date'), tz=timezone.utc),
                company=    company
            )

            if parsed_review.get('stars') <= 3:
                Notification.objects.create(
                    company=    review.company,
                    review=     review,
                    text=       review.text,
                    initiator=  Notification.Initiator.YANDEX_NEGATIVE_REVIEW
                )

        except:
            pass

    company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
    company.save()