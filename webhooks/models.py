from django.db import models


class TelegramSubscription(models.Model):
    class Meta:
        db_table = 'webhook_telegram_subscription'
        verbose_name = 'telegram подписка на оповещения'
        verbose_name_plural = 'telegram подписки на оповещения'
        unique_together = ['telegram_user_id', 'branch']

    telegram_user_id = models.CharField(
        max_length=255,
        verbose_name='ID пользователя telegram'
    )

    group = models.ForeignKey(
        'auth.Group',
        on_delete=models.CASCADE,
        verbose_name='группа'
    )

    branch = models.ForeignKey(
        'resources.Branch',
        on_delete=models.CASCADE,
        verbose_name='филиал'
    )

    def __str__(self):
        return (f'{self.group.name} / {self.branch.name} / {self.telegram_user_id}')
