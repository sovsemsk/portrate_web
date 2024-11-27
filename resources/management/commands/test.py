from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company
from spiders.yandex.case import perform as yandex_perform
from spiders.gis.case import perform as gis_perform
from spiders.google.case import perform as google_perform


class Command(BaseCommand):
    help = "Запуск всех парсеров"

    def handle(self, *args, **options):
        company = Company.objects.first()

        # yandex_perform(company.id)
        google_perform(company.id)
        # gis_perform(company.id)
