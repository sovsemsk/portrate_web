from django.contrib.auth.models import Group
from django.db import models
from resources.models import Branch

class ReviewsParser(models.Model):
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