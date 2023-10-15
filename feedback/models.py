from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch


class NegativeMessage(models.Model):
    class Meta:
        db_table = 'feedback_negative_message'
        verbose_name = 'негативное сообщение'
        verbose_name_plural = 'негативные сообщения'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа'
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='филиал'
    )

    phone = models.CharField(
        max_length=255,
        verbose_name='Контактный телефон'
    )

    text = models.TextField(
        verbose_name='Текст сообщения'
    )

    def __str__(self):
        return self.name


class NegativeReview(models.Model):
    class Meta:
        db_table = 'feedback_negative_review'
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
        db_table = 'feedback_positive_review'
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
