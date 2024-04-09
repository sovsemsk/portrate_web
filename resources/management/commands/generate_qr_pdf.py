from django.core.files import File
from django.core.management.base import BaseCommand

from pdf.qr import generate_stick
from resources.models import Company


class Command(BaseCommand):
    help = "Очистка старой истории рейтингов"

    def handle(self, *args, **options):
        companies = Company.objects.all()

        for company in companies:
            company.stick_light = File(generate_stick(company.id, "light"))
            company.stick_light.name = "stick_light.pdf"
            company.stick_dark = File(generate_stick(company.id, "dark"))
            company.stick_dark.name = "stick_dark.pdf"
            company.save()
