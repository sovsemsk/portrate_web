from django.core.management.base import BaseCommand

from resources.models import Company


class Command(BaseCommand):
	help = "Тест парсера"

	def handle(self, *args, **options):
		companies = Company.objects.all()

		for company in companies:
			print(company.is_active)
			print(company.can_parse_yandex)
