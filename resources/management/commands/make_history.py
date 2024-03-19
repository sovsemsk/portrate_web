import datetime
import random

from django.core.management import BaseCommand

from resources.models import RatingStamp


class Command(BaseCommand):
    help = "Парсинг карточек"

    def handle(self, *args, **options):
        start = datetime.datetime.strptime("01-01-2020", "%d-%m-%Y")
        end = datetime.datetime.strptime("01-01-2025", "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

        for date in date_generated:
            try:
                rs = RatingStamp(
                    created_at=date,
                    rating_yandex=random.uniform(0.0, 5.0),
                    rating_gis=random.uniform(0.0, 5.0),
                    rating_google=random.uniform(0.0, 5.0),
                    company_id=15
                )
                rs.save()
            except:
                print(date)
