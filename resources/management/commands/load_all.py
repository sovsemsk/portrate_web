from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import update_yandex_task, update_gis_task, update_google_task, update_counters_task


class Command(BaseCommand):
    help = "Запуск всех парсеров"

    def handle(self, *args, **options):
        companies = Company.objects.all()

        for company in companies:
            parsers_runs = False
            parsers_chain = []

            if company.is_parse_yandex:
                parsers_runs = True
                parsers_chain.append(update_yandex_task.s(company_id=company.id))

            if company.is_parse_gis:
                parsers_runs = True
                parsers_chain.append(update_gis_task.s(company_id=company.id))

            if company.is_parse_google:
                parsers_runs = True
                parsers_chain.append(update_google_task.s(company_id=company.id))

            if parsers_runs:
                parsers_chain.append(update_counters_task.s(company_id=company.id))
                chain(parsers_chain).apply_async()
