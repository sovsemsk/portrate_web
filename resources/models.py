from django.contrib.auth.models import Group
from django.db import models

class Branch(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    title = models.CharField()

    def __str__(self):
        return self.title

class Website(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    is_published = models.BooleanField(default=False)
    path_url = models.CharField(max_length=255, unique=True)
    info_title = models.CharField()
    info_city =  models.CharField()
    info_address = models.CharField()
    info_schedule = models.CharField()
    info_phone = models.CharField()
    info_description = models.TextField()
    info_website_url = models.CharField()
    action_website_url = models.CharField()
    action_title = models.CharField()
    stat_reviews_count = models.IntegerField(default=0)
    stat_reviews_rating = models.FloatField(default=0)

    def __str__(self):
        return self.info_title

class WebsiteImage(models.Model):
    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE
    )

    is_logo = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return self.title

class WebsiteExternalUrl(models.Model):

    class ExternalService(models.TextChoices):
        CUSTOM = "CUSTOM"
        VK = "VK"
        OK = "OK"
        X = "X"
        FACEBOOK = "FACEBOOK"
        INSTAGRAM = "INSTAGRAM"
        YOUTUBE = "YOUTUBE"
        VIMEO = "VIMEO"
        RUTUBE = "RUTUBE"

    external_service = models.CharField(
        max_length=255,
        choices=ExternalService.choices,
        default=ExternalService.CUSTOM,
    )

    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    url = models.CharField()

    def __str__(self):
        return self.title

class WebsiteExternalCard(models.Model):

    class ExternalService(models.TextChoices):
        CUSTOM = "CUSTOM"
        YANDEX = "YANDEX"
        GOOGLE = "GOOGLE"
        GIS = "GIS"

    external_service = models.CharField(
        max_length=255,
        choices=ExternalService.choices,
        default=ExternalService.CUSTOM,
    )

    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    url = models.CharField()

class WebsitePage(models.Model):
    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255)