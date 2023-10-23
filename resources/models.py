from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    class Meta:
        db_table = 'resources_company'
        verbose_name = 'сеть'
        verbose_name_plural = 'сети'

    user = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='пользователи'
    )

    name = models.CharField(
        verbose_name='название'
    )

    def __str__(self):
        return self.name


class Branch(models.Model):
    class Meta:
        db_table = 'resources_branch'
        verbose_name = 'филиал'
        verbose_name_plural = 'филиалы'

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        verbose_name='сеть'
    )

    name = models.CharField(
        verbose_name='название'
    )

    def __str__(self):
        return f'{self.company} - {self.name}'


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

    specialization = models.CharField(
        verbose_name='Специализация'
    )

    city = models.CharField(
        verbose_name='город'
    )

    address = models.CharField(
        verbose_name='адрес'
    )

    is_work_at_monday = models.BooleanField(
        default=True,
        verbose_name='работает в понедельник?'
    )

    is_work_at_tuesday = models.BooleanField(
        default=True,
        verbose_name='работает в вторник?'
    )

    is_work_at_wednesday = models.BooleanField(
        default=True,
        verbose_name='работает в среду?'
    )

    is_work_at_thursday = models.BooleanField(
        default=True,
        verbose_name='работает в четверг?'
    )

    is_work_at_friday = models.BooleanField(
        default=True,
        verbose_name='работает в пятницу?'
    )

    is_work_at_saturday = models.BooleanField(
        default=True,
        verbose_name='работает в субботу?'
    )

    is_work_at_sunday = models.BooleanField(
        default=True,
        verbose_name='работает в воскресенье?'
    )

    monday_schedule = models.CharField(
        verbose_name='часы работы в понедельник'
    )

    tuesday_schedule = models.CharField(
        verbose_name='часы работы во вторник'
    )

    wednesday_schedule = models.CharField(
        verbose_name='часы работы в среду'
    )

    thursday_schedule = models.CharField(
        verbose_name='часы работы в четверг'
    )

    friday_schedule = models.CharField(
        verbose_name='часы работы в пятницу'
    )

    saturday_schedule = models.CharField(
        verbose_name='часы работы в субботу'
    )

    sunday_schedule = models.CharField(
        verbose_name='часы работы в воскресенье'
    )

    description = models.TextField(
        verbose_name='описание'
    )

    action_button_text = models.CharField(
        verbose_name='текст кнопки действия'
    )

    action_button_url = models.CharField(
        verbose_name='url кнопки действия'
    )

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        verbose_name='сеть'
    )

    branch = models.OneToOneField(
        'Branch',
        on_delete=models.CASCADE,
        verbose_name='филиал'
    )

    # @TODO: N+1, использовать только для одной записи
    @property
    def logo(self):
        return WebsiteImage.objects.filter(website=self, is_logo=True).first

    # @TODO: N+1, использовать только для одной записи
    @property
    def phone(self):
        return WebsiteContact.objects.filter(website=self, platform='PHONE').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def website(self):
        return WebsiteUrl.objects.filter(website=self, platform='WEBSITE').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def vk(self):
        return WebsiteUrl.objects.filter(website=self, platform='VK').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def ok(self):
        return WebsiteUrl.objects.filter(website=self, platform='OK').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def x(self):
        return WebsiteUrl.objects.filter(website=self, platform='X').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def facebook(self):
        return WebsiteUrl.objects.filter(website=self, platform='FACEBOOK').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def instagram(self):
        return WebsiteUrl.objects.filter(website=self, platform='INSTAGRAM').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def youtube(self):
        return WebsiteUrl.objects.filter(website=self, platform='YOUTUBE').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def rutube(self):
        return WebsiteUrl.objects.filter(website=self, platform='RUTUBE').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def email(self):
        return WebsiteContact.objects.filter(website=self, platform='EMAIL').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def whatsapp(self):
        return WebsiteContact.objects.filter(website=self, platform='WHATSAPP').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def telegram(self):
        return WebsiteContact.objects.filter(website=self, platform='TELEGRAM').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def viber(self):
        return WebsiteContact.objects.filter(website=self, platform='VIBER').first

    # @TODO: N+1, использовать только для одной записи
    @property
    def images(self):
        return self.websiteimage_set.filter(is_logo=False).order_by('sort').all()

    # @TODO: N+1, использовать только для одной записи
    @property
    def contacts(self):
        return self.websitecontact_set.all()

    # @TODO: N+1, использовать только для одной записи
    @property
    def urls(self):
        return self.websiteurl_set.all()

    # @TODO: N+1, использовать только для одной записи
    @property
    def cards(self):
        return self.websitecard_set.all()

    def __str__(self):
        return self.name


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
        return self.name


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
        return self.name


class WebsiteUrl(models.Model):
    class Meta:
        db_table = 'resources_website_url'
        verbose_name = 'ссылка вебсайта'
        verbose_name_plural = 'ссылки вебсайта'

    class Platform(models.TextChoices):
        CUSTOM = 'CUSTOM'
        WEBSITE = 'WEBSITE'
        VK = 'VK'
        OK = 'OK'
        X = 'X'
        FACEBOOK = 'FACEBOOK'
        INSTAGRAM = 'INSTAGRAM'
        YOUTUBE = 'YOUTUBE'
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
        return self.name


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
        DIKIDI = 'DIKIDI'
        RESTOCLUB = 'RESTOCLUB'
        TRIPADVISOR = 'TRIPADVISOR'
        PRODOCTOROV = 'PRODOCTOROV'
        FLAMP = 'FLAMP'
        ZOON = 'ZOON'
        OTZOVIK = 'OTZOVIK'
        IRECOMMEND = 'IRECOMMEND'

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
        verbose_name='ссылка на карточку'
    )

    website = models.ForeignKey(
        'Website',
        on_delete=models.CASCADE,
        verbose_name='вебсайт'
    )

    def __str__(self):
        return f'{self.website} / {self.name}'


class NegativeMessageTag(models.Model):
    class Meta:
        db_table = 'resources_negative_message_tag'
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
        db_table = 'resources_negative_message'
        verbose_name = 'негативное сообщение'
        verbose_name_plural = 'негативные сообщения'

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='сеть'
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
        db_table = 'resources_negative_review'
        verbose_name = 'негативный отзыв'
        verbose_name_plural = 'негативные отзывы'

    company = models.ForeignKey(
        Company,
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
        db_table = 'resources_positive_review'
        verbose_name = 'позитивный отзыв'
        verbose_name_plural = 'позитивные отзывы'

    company = models.ForeignKey(
        Company,
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
