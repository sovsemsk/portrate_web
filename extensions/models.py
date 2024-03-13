import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django_celery_results.models import TaskResult


class Timezone(models.TextChoices):
    """ Часовой пояс """

    UTC = "UTC", "UTC"
    Europe_Moscow = "Europe/Moscow", "Москва"
    Asia_Yekaterinburg = "Asia/Yekaterinburg", "Екатеринбург"


class Profile(models.Model):
    """ Профиль """

    class Meta:
        db_table = "extensions_profile"
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    """ Автогенерация """
    api_secret = models.CharField(verbose_name="API ключ", db_index=True)

    """ Настройки """
    can_notify_at_start = models.TimeField(blank=True, default=datetime.time(9, 00), null=True, verbose_name="можно оповещать с")
    can_notify_at_end = models.TimeField(blank=True, default=datetime.time(17, 00), null=True, verbose_name="можно оповещать до")
    can_notify_negative_portrate = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о сообщениях в Портрет")
    can_notify_negative_yandex = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в Яндекс Карты")
    can_notify_negative_gis = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в 2Гис Карты")
    can_notify_negative_google = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в Google Maps")
    default_timezone = models.CharField(blank=False, null=False, choices=Timezone.choices, default=Timezone.UTC, verbose_name="Временная зона по умолчанию")
    telegram_id = models.CharField(blank=True, null=True, verbose_name="telegram ID")

    """ Связи """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_init, sender=Profile)
def profile_post_init(sender, instance, **kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_init, sender=TaskResult)
def task_result_post_init(sender, instance, **kwargs):
    pass