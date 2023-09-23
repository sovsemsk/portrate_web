from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch

class LinkIntegration(models.Model):
    class Meta:
        verbose_name = 'Интеграция с файлом'
        verbose_name_plural = 'Интеграции с файлом'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()

    def __str__(self):
        return self.name

class IikoIntegration(models.Model):
    class Meta:
        verbose_name = 'Интеграция с Iiko Cloud'
        verbose_name_plural = 'Интеграции с Iiko Cloud'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()

    def __str__(self):
        return self.name

class Bitrix24Integration(models.Model):
    class Meta:
        verbose_name = 'Интеграция с Bitrix24'
        verbose_name_plural = 'Интеграции с Bitrix24'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()

    def __str__(self):
        return self.name

class YclientsIntegration(models.Model):
    class Meta:
        verbose_name = 'Интеграция с Yclients'
        verbose_name_plural = 'Интеграции с Yclients'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()

    def __str__(self):
        return self.name

class TopnlabIntegration(models.Model):
    class Meta:
        verbose_name = 'Интеграция с Topnlab'
        verbose_name_plural = 'Интеграции с Topnlab'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()

    def __str__(self):
        return self.name
