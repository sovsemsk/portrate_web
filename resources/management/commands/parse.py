from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import parse_gis_rate, parse_gis_reviews, parse_yandex_rate, parse_yandex_reviews, \
    send_telegram_text_task


class Command(BaseCommand):
    help = "Парсинг (загрузка) данных"

    def add_arguments(self, parser):
        parser.add_argument("-rt", "--rating", action="store_true", default=False, help="Парсинг рейтинга")
        parser.add_argument("-rv", "--reviews", action="store_true", default=False, help="Парсинг отзывов")
        parser.add_argument("-ya", "--yandex", action="store_true", default=False, help="Парсинг Яндекс")
        parser.add_argument("-gi", "--gis", action="store_true", default=False, help="Парсинг 2Гис")
        parser.add_argument("-tg", "--telegram", action="store_true", default=False, help="Telegram test")

    def handle(self, *args, **options):
        if options["telegram"]:
            send_telegram_text_task("5304013231", "TEST")

        # Рейтинг Яндекс
        if options["yandex"] and options["rating"]:
            companies = Company.objects.filter(is_active=True, is_yandex_reviews_download=True).exclude(yandex_parser_link=None).values("id").all()

            for company in companies:
                parse_yandex_rate.delay(company["id"])

        # Отзывы Яндекс
        if options["yandex"] and options["reviews"]:
            companies = Company.objects.filter(is_active=True, is_yandex_reviews_download=True).exclude(yandex_parser_link=None).values("id").all()

            for company in companies:
                parse_yandex_reviews.delay(company["id"])

        # Рейтинг 2Гис
        if options["gis"] and options["rating"]:
            companies = Company.objects.filter(is_active=True, is_gis_reviews_download=True).exclude(gis_parser_link=None).values("id").all()

            for company in companies:
                parse_gis_rate.delay(company["id"])

        # Отзывы 2Гис
        if options["gis"] and options["reviews"]:
            companies = Company.objects.filter(is_active=True, is_gis_reviews_download=True).exclude(gis_parser_link=None).values("id").all()

            for company in companies:
                parse_gis_reviews.delay(company["id"])
