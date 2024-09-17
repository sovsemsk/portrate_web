from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from djmoney.money import Money


class Command(BaseCommand):
    help = "Списание ежедневного баланса"

    def handle(self, *args, **options):
        users = User.objects.select_related("profile").all()

        for user in users:
            if user.profile.is_active:
                user.profile.balance = Money(float(user.profile.balance.amount) - user.profile.day_price, "RUB")
                user.save()
