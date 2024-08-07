from celery import chain
from django.core.management.base import BaseCommand

from resources.models import Company, Review
from resources.tasks import parse_yandex_task, parse_gis_task, parse_google_task


class Command(BaseCommand):
	help = "Тест парсера"

	def handle(self, *args, **options):
		print(len("ул. Ленинского Комсомола, 4Б, Орск, Оренбургская обл., Россия, 462420"))
		# parsers_chain = []
		# company = Company.objects.get(pk=22)

		# if company.parser_link_yandex:
		# 	parsers_chain.append(parse_yandex_task.s(company_id=company.id))

		# if company.parser_link_gis:
		# 	parsers_chain.append(parse_gis_task.s(company_id=company.id))

		# if company.parser_link_google:
		# 	parsers_chain.append(parse_google_task.s(company_id=company.id))

		# chain(*parsers_chain).apply_async()
