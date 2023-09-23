from django.db import models

from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch
from feedback.models import NegativeMessage, NegativeReview

class NegativeMessageEvent(models.Model):
    class Meta:
        verbose_name = 'Сообытие негативного сообщения'
        verbose_name_plural = 'Сообытия негативного сообщения'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    negative_message = models.ForeignKey(
        NegativeMessage,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.branch.title

class NegativeReviewEvent(models.Model):
    class Meta:
        verbose_name = 'Сообытие негативного отзыва'
        verbose_name_plural = 'Сообытия негативного отзыва'

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    negative_review = models.ForeignKey(
        NegativeReview,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.branch.title
