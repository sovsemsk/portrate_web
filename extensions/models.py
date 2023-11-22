from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


class Profile(models.Model):
    class Meta:
        db_table = 'extensions_profile'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
    
    class DefaultTimezone(models.TextChoices):
        UTC = 'UTC', 'UTC'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    api_secret = models.CharField(
        verbose_name='API ключ'
    )

    telegram_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='telegram ID'
    )

    default_timezone = models.CharField(
        blank=True,
        null=True,
        choices=DefaultTimezone.choices,
        default=DefaultTimezone.UTC,
        verbose_name='Временная зона по умолчанию'
    )

    can_notify_at_start = models.TimeField(
        blank=True,
        null=True,
        verbose_name='можно оповещать с'
    )

    can_notify_at_end = models.TimeField(
        blank=True,
        null=True,
        verbose_name='можно оповещать до'
    )

    can_notify_negative_portrate = models.BooleanField(
        blank=True,
        default=True,
        null=True,
        verbose_name='получать оповещения в Telegram о негативных сообщениях в Портрет'
    )

    can_notify_negative_yandex = models.BooleanField(
        blank=True,
        default=True,
        null=True,
        verbose_name='получать оповещения в Telegram о негативных отзывах в Яндекс Карты'
    )

    can_notify_negative_gis = models.BooleanField(
        blank=True,
        default=True,
        null=True,
        verbose_name='получать оповещения в Telegram о негативных отзывах в 2Гис Карты'
    )

    can_notify_negative_google = models.BooleanField(
        blank=True,
        default=True,
        null=True,
        verbose_name='получать оповещения в Telegram о негативных отзывах в Google Maps'
    )

    def __str__(self):
        return self.user.username


# Сигналы модели User
@receiver(post_save, sender=User)
def create_or_update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Сигналы модели Profile
@receiver(post_init, sender=Profile)
def init_api_secret_signal(sender, instance, ** kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)
