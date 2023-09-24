from django.contrib.auth.models import Group
from django.db import models


class Branch(models.Model):
    class Meta:
        db_table = 'resources_branch'
        verbose_name = 'филиал'
        verbose_name_plural = 'филиалы'

    name = models.CharField(
        verbose_name='название'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа'
    )

    def __str__(self):
        return f'{self.group.name} / {self.name}'


class Website(models.Model):
    class Meta:
        db_table = 'resources_website'
        verbose_name = 'вебсайт'
        verbose_name_plural = 'вебсайты'

    is_published = models.BooleanField(
        default=False,
        verbose_name='опубликовано?'
    )

    path = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='поддомен'
    )

    name = models.CharField(
        verbose_name='название'
    )

    city = models.CharField(
        verbose_name='город'
    )

    address = models.CharField(
        verbose_name='адрес'
    )

    schedule = models.CharField(
        verbose_name='график работы'
    )

    description = models.TextField(
        verbose_name='описание'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='группа'
    )

    branch = models.ForeignKey(
        'Branch',
        on_delete=models.CASCADE,
        verbose_name='филиал'
    )

    def __str__(self):
        return f'{self.group.name} / {self.name}'

    # @TODO: N+1, использовать только для одной записи
    @property
    def logo(self):
        return WebsiteImage.objects.filter(website=self, is_logo=True).first

    # @TODO: N+1, использовать только для одной записи
    @property
    def images(self):
        return WebsiteImage.objects.filter(website=self, is_logo=False).order_by('sort').all


class WebsiteImage(models.Model):
    class Meta:
        db_table = 'resources_website_image'
        verbose_name = 'изображение вебсайта'
        verbose_name_plural = 'изображения вебсайта'

    is_logo = models.BooleanField(
        default=False,
        verbose_name='логотип?'
    )

    sort = models.IntegerField(
        default=0,
        verbose_name='порядок'
    )

    file = models.ImageField(
        upload_to='website_images/%Y/%m/%d/',
        verbose_name='файл'
    )

    name = models.CharField(
        verbose_name='название'
    )

    website = models.ForeignKey(
        'Website',
        on_delete=models.CASCADE,
        verbose_name='вебсайт'
    )

    def __str__(self):
        return f'{self.website} / {self.name}'


class WebsiteContact(models.Model):
    class Meta:
        db_table = 'resources_website_contact'
        verbose_name = 'контакт вебсайта'
        verbose_name_plural = 'контакты вебсайта'

    class Platform(models.TextChoices):
        CUSTOM = 'CUSTOM'
        PHONE = 'PHONE'
        WHATSAPP = 'WHATSAPP'
        TELEGRAM = 'TELEGRAM'
        VIBER = 'VIBER'
        EMAIL = 'EMAIL'

    platform = models.CharField(
        choices=Platform.choices,
        default=Platform.CUSTOM,
        verbose_name='тип'
    )

    name = models.CharField(
        blank=True,
        verbose_name='название'
    )

    value = models.CharField(
        verbose_name='контакт'
    )

    website = models.ForeignKey(
        'Website',
        on_delete=models.CASCADE,
        verbose_name='вебсайт'
    )

    def __str__(self):
        return f'{self.website} / {self.name}'


class WebsiteUrl(models.Model):
    class Meta:
        db_table = 'resources_website_url'
        verbose_name = 'ссылка вебсайта'
        verbose_name_plural = 'ссылки вебсайта'

    class Platform(models.TextChoices):
        CUSTOM = 'CUSTOM'
        VK = 'VK'
        OK = 'OK'
        X = 'X'
        FACEBOOK = 'FACEBOOK'
        INSTAGRAM = 'INSTAGRAM'
        YOUTUBE = 'YOUTUBE'
        VIMEO = 'VIMEO'
        RUTUBE = 'RUTUBE'

    platform = models.CharField(
        choices=Platform.choices,
        default=Platform.CUSTOM,
        verbose_name='тип'
    )

    name = models.CharField(
        blank=True,
        verbose_name='название'
    )

    value = models.CharField(
        verbose_name='ссылка на ресурс'
    )

    website = models.ForeignKey(
        'Website',
        on_delete=models.CASCADE,
        verbose_name='вебсайт'
    )

    def __str__(self):
        return f'{self.website} / {self.name}'


class WebsiteCard(models.Model):
    class Meta:
        db_table = 'resources_website_card'
        verbose_name = 'карточка вебсайта'
        verbose_name_plural = 'карточки вебсайта'

    class Platform(models.TextChoices):
        CUSTOM = 'CUSTOM'
        YANDEX = 'YANDEX'
        GOOGLE = 'GOOGLE'
        GIS = 'GIS'
        MAPSME = 'MAPSME'

    platform = models.CharField(
        choices=Platform.choices, default=Platform.CUSTOM, verbose_name='тип')
    name = models.CharField(blank=True, verbose_name='название')
    value = models.CharField(verbose_name='ссылка на карточку')

    website = models.ForeignKey(
        'Website', on_delete=models.CASCADE, verbose_name='вебсайт')

    def __str__(self):
        return f'{self.website} / {self.name}'


class WebsitePage(models.Model):
    class Meta:
        db_table = 'resources_website_page'
        verbose_name = 'страница вебсайта'
        verbose_name_plural = 'страницы вебсайта'

    name = models.CharField(verbose_name='название')
    value = models.TextField(verbose_name='значение')

    website = models.ForeignKey(
        'Website', on_delete=models.CASCADE, verbose_name='вебсайт')

    def __str__(self):
        return f'{self.website} / {self.name}'
