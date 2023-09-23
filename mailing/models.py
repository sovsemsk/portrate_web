from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch
from resources.models import Branch

class PhoneMessage(models.Model):
    class Meta:
        verbose_name = 'Сообщение на телефон'
        verbose_name_plural = 'Сообщения на телефон'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    phone = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.phone

class EmailMessage(models.Model):
    class Meta:
        verbose_name = 'Сообщение на почту'
        verbose_name_plural = 'Сообщения на почту'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    email = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.phone

class TelegramMessage(models.Model):
    class Meta:
        verbose_name = 'Сообщение на telegram'
        verbose_name_plural = 'Сообщения на telegram'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    email = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.phone

class WhatsappMessage(models.Model):
    class Meta:
        verbose_name = 'Сообщение на whatsapp'
        verbose_name_plural = 'Сообщения на whatsapp'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    email = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.phone
