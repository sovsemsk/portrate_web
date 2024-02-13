from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import parse_cards


class Command(BaseCommand):
    help = "Парсинг (загрузка) данных"

    def handle(self, *args, **options):
        companies = Company.objects.filter(is_active=True).values("id").all()

        for company in companies:
            parse_cards.delay(company["id"])
