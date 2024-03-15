import asyncio
from datetime import datetime, timezone

from celery import shared_task
from django.conf import settings
from django.db import IntegrityError
from telegram import Bot

from parsers.parser_gis import ParserGis
from parsers.parser_google import ParserGoogle
from parsers.parser_yandex import ParserYandex
from resources.models import Company, Review, RatingStamp, Service


@shared_task(name="send telegram")
def send_telegram_text_task(telegram_id, text):
    asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(telegram_id, text))
    return f"Done send to {telegram_id}"


@shared_task(name="parse cards")
def parse_cards(company_id):
    company = Company.objects.get(id=company_id, is_active=True)
    rating_history = RatingStamp(company_id=company.id)

    """ Яндекс """
    if company.is_parse_yandex:
        yandex_parser = ParserYandex(company.parser_link_yandex)

        """ Проверка страницы Яндекс """
        if yandex_parser.check_page():

            """ Парсинг рейтинга Яндекс """
            rating_yandex = yandex_parser.parse_rating()
            company.rating_yandex = rating_yandex
            company.rating_yandex_last_parse_at = datetime.now(timezone.utc)
            """ Парсинг отзывов Яндекс """
            for review_yandex in yandex_parser.parse_reviews():
                try:
                    Review.objects.create(
                        company=company,
                        created_at=review_yandex["created_at"],
                        name=review_yandex["name"],
                        remote_id=review_yandex["remote_id"],
                        service=Service.YANDEX,
                        stars=review_yandex["stars"],
                        text=review_yandex["text"]
                    )
                except IntegrityError:
                    pass

            company.reviews_yandex_last_parse_at = datetime.now(timezone.utc)

        """ Закрытие страницы Яндекс """
        yandex_parser.close_page()

        """ Подсчет агрегаций Яндекс """
        company.reviews_yandex_negative_count = Review.objects.filter(company_id=company_id, service=Service.YANDEX, stars__lte=3).count()
        company.reviews_yandex_positive_count = Review.objects.filter(company_id=company_id, service=Service.YANDEX, stars__gt=3).count()
        company.reviews_yandex_total_count = Review.objects.filter(company_id=company_id, service=Service.YANDEX).count()

    """ 2Гис """
    if company.is_parse_gis:
        gis_parser = ParserGis(company.parser_link_gis)

        """ Проверка страницы 2Гис """
        if gis_parser.check_page():

            """ Парсинг рейтинга 2Гис """
            rating_gis = gis_parser.parse_rating()
            company.rating_gis = rating_gis
            company.rating_gis_last_parse_at = datetime.now(timezone.utc)

            """ Парсинг отзывов 2Гис """
            for review_gis in gis_parser.parse_reviews():
                try:
                    Review.objects.create(
                        company=company,
                        created_at=review_gis["created_at"],
                        name=review_gis["name"],
                        remote_id=review_gis["remote_id"],
                        service=Service.GIS,
                        stars=review_gis["stars"],
                        text=review_gis["text"]
                    )
                except IntegrityError:
                    pass
            company.reviews_gis_last_parse_at = datetime.now(timezone.utc)

        """ Закрытие страницы Яндекс """
        gis_parser.close_page()

        """ Подсчет агрегаций Яндекс """
        company.reviews_gis_negative_count = Review.objects.filter(company_id=company_id, service=Service.GIS, stars__lte=3).count()
        company.reviews_gis_positive_count = Review.objects.filter(company_id=company_id, service=Service.GIS, stars__gt=3).count()
        company.reviews_gis_total_count = Review.objects.filter(company_id=company_id, service=Service.GIS).count()

    """ Google """
    if company.is_parse_google:
        google_parser = ParserGoogle(company.parser_link_google)

        """ Проверка страницы Google """
        if google_parser.check_page():

            """ Парсинг рейтинга Google """
            rating_google = google_parser.parse_rating()
            company.rating_google = rating_google
            company.rating_google_last_parse_at = datetime.now(timezone.utc)

            """ Парсинг отзывов Google """
            for review_google in google_parser.parse_reviews():
                if review_google["text"]:
                    try:
                        Review.objects.create(
                            company=company,
                            created_at=review_google["created_at"],
                            name=review_google["name"],
                            remote_id=review_google["remote_id"],
                            service=Service.GOOGLE,
                            stars=review_google["stars"],
                            text=review_google["text"]
                        )
                    except IntegrityError:
                        pass

            company.reviews_google_last_parse_at = datetime.now(timezone.utc)

        """ Закрытие страницы Google """
        google_parser.close_page()

        """ Подсчет агрегаций Google """
        company.reviews_google_negative_count = Review.objects.filter(company_id=company_id, service=Service.GOOGLE, stars__lte=3).count()
        company.reviews_google_positive_count = Review.objects.filter(company_id=company_id, service=Service.GOOGLE, stars__gt=3).count()
        company.reviews_google_total_count = Review.objects.filter(company_id=company_id, service=Service.GOOGLE).count()

    """ Подсчет агрегаций """
    company.reviews_total_count = Review.objects.filter(company_id=company_id).count()
    company.rating = max([company.rating_yandex, company.rating_gis, company.rating_google])

    """ Фиксация истории для графика динамики """
    rating_history.rating_yandex = company.rating_yandex
    rating_history.rating_gis = company.rating_gis
    rating_history.rating_google = company.rating_google
    rating_history.save()

    """ Сохранение компании """
    company.is_first_parsing = False
    company.save()
    return f"Done for Company #{company_id}"

