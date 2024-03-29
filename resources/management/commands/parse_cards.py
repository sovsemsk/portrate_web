from django.core.management.base import BaseCommand

from resources.models import Company
from resources.tasks import parse_cards_task


class Command(BaseCommand):
    help = "Парсинг карточек"

    def handle(self, *args, **options):
        companies = Company.objects.filter(is_active=True).values("id").all()

        for company in companies:
            parse_cards_task.delay(company["id"])
