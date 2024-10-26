import re

from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import (
    parse_yandex_task,
    parse_gis_task,
    parse_google_task,
    parse_avito_task,
    parse_zoon_task,
)


class Command(BaseCommand):
    help = "Запуск всех парсеров"

    def handle(self, *args, **options):
        company = Company.objects.first()
        parsers_chain = []
        # parsers_chain.append(parse_yandex_task.s(company_id=company.id))
        # parsers_chain.append(parse_gis_task.s(company_id=company.id))
        # parsers_chain.append(parse_google_task.s(company_id=company.id))
        # parsers_chain.append(parse_avito_task.s(company_id=company.id))
        parsers_chain.append(parse_zoon_task.s(company_id=company.id))
        chain(* parsers_chain).apply_async()

