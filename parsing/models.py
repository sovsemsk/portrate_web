from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch

class ReviewsParser(models.Model):
    class Meta:
        verbose_name = 'Парсер отзывов'
        verbose_name_plural = 'Парсеры отзывов'

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

class RatingParser(models.Model):
    class Meta:
        verbose_name = 'Парсер рейтинга'
        verbose_name_plural = 'Парсеры рейтинга'

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