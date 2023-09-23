from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch

class NegativeMessage(models.Model):
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