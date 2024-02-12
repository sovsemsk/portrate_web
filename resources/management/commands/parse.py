from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import parse_yandex, parse_gis, send_telegram_text_task


class Command(BaseCommand):
    help = "Парсинг (загрузка) данных"

    def add_arguments(self, parser):
        parser.add_argument("-tg", "--telegram", action="store_true", default=False, help="Telegram test")
        parser.add_argument("-ya", "--yandex", action="store_true", default=False, help="Парсинг Яндекс")
        parser.add_argument("-gi", "--gis", action="store_true", default=False, help="Парсинг 2Гис")

    def handle(self, *args, **options):
        if options["telegram"]:
            send_telegram_text_task("5304013231", "TEST")

        # Парсинг Яндекс
        if options["yandex"]:
            companies = Company.objects.filter(is_active=True, is_yandex_reviews_download=True).exclude(yandex_parser_link=None).values("id").all()

            for company in companies:
                parse_yandex.delay(company["id"])

        # Парсинг 2Гис
        if options["gis"]:
            companies = Company.objects.filter(is_active=True, is_gis_reviews_download=True).exclude(gis_parser_link=None).values("id").all()

            for company in companies:
                parse_gis.delay(company["id"])
