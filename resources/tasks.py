import asyncio
from datetime import datetime, timezone, timedelta

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

    date_week_ago = datetime.today() - timedelta(days=7)
    date_month_ago = datetime.today() - timedelta(days=30)
    date_quarter_ago = datetime.today() - timedelta(days=90)
    date_year_ago = datetime.today() - timedelta(days=365)

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
                if review_yandex["text"]:
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
        reviews_yandex = Review.objects.filter(company_id=company_id, service=Service.YANDEX)
        #
        company.reviews_yandex_negative_count = reviews_yandex.filter(stars__lte=3).count()
        company.reviews_yandex_negative_week_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_negative_month_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_negative_quarter_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_negative_year_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_yandex_positive_count = reviews_yandex.filter(stars__gt=3).count()
        company.reviews_yandex_positive_week_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_positive_month_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_positive_quarter_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_positive_year_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_yandex_total_count = reviews_yandex.count()
        company.reviews_yandex_total_week_count = reviews_yandex.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_total_month_count = reviews_yandex.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_total_quarter_count = reviews_yandex.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_yandex_total_year_count = reviews_yandex.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

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
                if review_gis["text"]:
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

        """ Закрытие страницы 2Гис """
        gis_parser.close_page()

        """ Подсчет агрегаций 2Гис """
        reviews_gis = Review.objects.filter(company_id=company_id, service=Service.GIS)
        #
        company.reviews_gis_negative_count = reviews_gis.filter(stars__lte=3).count()
        company.reviews_gis_negative_week_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_negative_month_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_negative_quarter_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_negative_year_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_gis_positive_count = reviews_gis.filter(stars__gt=3).count()
        company.reviews_gis_positive_week_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_positive_month_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_positive_quarter_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_positive_year_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_gis_total_count = reviews_gis.count()
        company.reviews_gis_total_week_count = reviews_gis.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_total_month_count = reviews_gis.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_total_quarter_count = reviews_gis.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_gis_total_year_count = reviews_gis.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

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
        reviews_google = Review.objects.filter(company_id=company_id, service=Service.GOOGLE)
        #
        company.reviews_google_negative_count = reviews_google.filter(stars__lte=3).count()
        company.reviews_google_negative_week_count = reviews_google.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_negative_month_count = reviews_google.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_negative_quarter_count = reviews_google.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_negative_year_count = reviews_google.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_google_positive_count = reviews_google.filter(stars__gt=3).count()
        company.reviews_google_positive_week_count = reviews_google.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_positive_month_count = reviews_google.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_positive_quarter_count = reviews_google.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_positive_year_count = reviews_google.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()
        #
        company.reviews_google_total_count = reviews_google.count()
        company.reviews_google_total_week_count = reviews_google.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_total_month_count = reviews_google.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_total_quarter_count = reviews_google.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
        company.reviews_google_total_year_count = reviews_google.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    """ Подсчет агрегаций """
    company.reviews_total_count = Review.objects.filter(company_id=company_id).count()
    company.rating = max([company.rating_yandex, company.rating_gis, company.rating_google])

    """ Фиксация истории для графика динамики """
    try:
        rating_history = RatingStamp(
            company_id=company.id,
            rating_yandex=company.rating_yandex,
            rating_gis=company.rating_gis,
            rating_google=company.rating_google
        )
        rating_history.save()
    except:
        pass

    """ Сохранение компании """
    company.is_first_parsing = False
    company.save()
    return f"Done for Company #{company_id}"

