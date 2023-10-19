from django.contrib.auth.models import User
from django.db import models


class TelegramSubscription(models.Model):
    class Meta:
        db_table = 'webhook_telegram_subscription'
        verbose_name = 'telegram подписка на оповещения'
        verbose_name_plural = 'telegram подписки на оповещения'

    telegram_user_id = models.CharField(
        max_length=255,
        verbose_name='ID пользователя telegram'
    )

    branch = models.OneToOneField(
        'resources.Branch',
        on_delete=models.CASCADE,
        verbose_name='филиал'
    )

    def __str__(self):
        return self.text
