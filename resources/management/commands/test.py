from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import parse_avito_task


class Command(BaseCommand):
	help = "Тест парсера"

	def handle(self, *args, **options):
		companies = Company.objects.all()

		for company in companies:
			parsers_chain = []

			if company.parser_link_avito:
				parsers_chain.append(parse_avito_task.s(company_id=company.id))

			chain(* parsers_chain).apply_async()