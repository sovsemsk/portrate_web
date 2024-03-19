from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Очистка старой истории рейтингов"

    def handle(self, *args, **options):
        pass
