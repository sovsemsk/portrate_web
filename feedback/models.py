from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch

class NegativeMessage(models.Model):
    class Meta:
        verbose_name = 'Негативное сообщение'
        verbose_name_plural = 'Негативные сообщения'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()
    phone = models.CharField()
    text = models.TextField()

    def __str__(self):
        return self.name

class NegativeReview(models.Model):
    class Meta:
        verbose_name = 'Негативный отзыв'
        verbose_name_plural = 'Негативные отзывы'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()
    text = models.TextField()

    def __str__(self):
        return self.name

class PositiveReview(models.Model):
    class Meta:
        verbose_name = 'Позитивный отзыв'
        verbose_name_plural = 'Позитивные отзывы'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField()
    text = models.TextField()

    def __str__(self):
        return self.name