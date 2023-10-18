from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch


class NegativeMessageTag(models.Model):
    class Meta:
        db_table = 'feedback_negative_message_tag'
        verbose_name = 'тег негативного сообщения'
        verbose_name_plural = 'теги негативного сообщения'

    text = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='текст тега'
    )

    def __str__(self):
        return self.text


class NegativeMessage(models.Model):
    class Meta:
        db_table = 'feedback_negative_message'
        verbose_name = 'негативное сообщение'
        verbose_name_plural = 'негативные сообщения'

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

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
        verbose_name='контактный телефон'
    )

    text = models.TextField(
        blank=True,
        verbose_name='текст сообщения'
    )

    negative_message_tag = models.ManyToManyField(
        NegativeMessageTag,
        blank=True,
        verbose_name='теги негативных сообщений'
    )

    def __str__(self):
        return self.phone


class NegativeReview(models.Model):
    class Meta:
        db_table = 'feedback_negative_review'
        verbose_name = 'негативный отзыв'
        verbose_name_plural = 'негативные отзывы'

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
        verbose_name = 'позитивный отзыв'
        verbose_name_plural = 'позитивные отзывы'

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
