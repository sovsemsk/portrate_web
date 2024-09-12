import math

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from djmoney.money import Money


class Command(BaseCommand):
    help = "Списание ежедневного баланса"

    def handle(self, *args, **options):
        users = User.objects.select_related("profile").all()

        for user in users:
            day_price = round(float(user.profile.__getattribute__(f"{user.profile.rate.lower()}_price_annually") / 365), 2)

            if user.profile.balance.amount > day_price:
                user.profile.balance = Money(float(user.profile.balance.amount) - day_price, "RUB")
            else:
                user.profile.balance = Money(0, "RUB")

            user.save()
