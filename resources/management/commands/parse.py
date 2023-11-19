from django.conf import settings
from django.core.management.base import BaseCommand


from resources.tasks import parse_yandex_rate, parse_yandex_reviews
from resources.models import Company


class Command(BaseCommand):
    help = 'Парсинг (загрузка) данных'


    def add_arguments(self, parser):
        parser.add_argument(
            '-rt',
            '--rating',
            action='store_true',
            default=False,
            help='Парсинг рейтинга'
        )

        parser.add_argument(
            '-rv',
            '--reviews',
            action='store_true',
            default=False,
            help='Парсинг отзывов'
        )

        parser.add_argument(
            '-ya',
            '--yandex',
            action='store_true',
            default=False,
            help='Парсинг Яндекс'
        )


    def handle(self, *args, **options):
        companies = Company.objects.exclude(
            yandex_id=None
        ).filter(
            is_active=True,
            is_yandex_reviews_download=True
        ).values('id').all()

        if options['rating']:
            if options['yandex']:
                for company in companies:
                    parse_yandex_rate.delay(company['id'])

        if options['reviews']:
            if options['yandex']:
                for company in companies:
                    parse_yandex_reviews.delay(company['id'])
