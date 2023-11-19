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
    from resources.models import Company, Review

    company = Company.objects.get(pk=company_id)

    parser = YandexParser(settings.SELENIUM_BOT_API_SECRET, int(company.yandex_id))
    result = parser.parse(type_parse='reviews')

    for review in result.get('company_reviews', None):
        id = hashlib.md5(
            f"{review.get('name')}{review.get('date')}".encode()
        ).hexdigest()

        try:
            Review.objects.create(
                name=review.get('name'),
                text=review.get('text'),
                answer=review.get('answer'),
                rate=review.get('stars'),
                remote_id=id,
                avatar_url=review.get('icon_href'),
                created_at=datetime.fromtimestamp(review.get('date'), tz=timezone.utc),
                company=company
            )
        except:
            pass

    company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
    company.save()