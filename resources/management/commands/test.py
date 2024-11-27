from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company
import resources.tasks as tasks

class Command(BaseCommand):
    help = "Запуск всех парсеров"

    def handle(self, *args, **options):
        company = Company.objects.first()

        parsers_chain = [
            # tasks.parse_yandex_task.s(company_id=company.id),
            # tasks.parse_gis_task.s(company_id=company.id),
            # tasks.parse_google_task.s(company_id=company.id)
        ]

        chain(* parsers_chain).apply_async()

