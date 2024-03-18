import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


class Service(models.TextChoices):
    """ Сервис """
    YANDEX = "YANDEX", "Яндекс"
    GIS = "GIS", "2Гис"
    GOOGLE = "GOOGLE", "Google"


class Stars(models.TextChoices):
    """ Звезды """
    _0 = "0", "0 звезд"
    _1 = "1", "1 звезда"
    _2 = "2", "2 звезды"
    _3 = "3", "3 звезды"
    _4 = "4", "4 звезды"
    _5 = "5", "5 звезд"


class Timezone(models.TextChoices):
    """ Часовой пояс """
    UTC = "UTC", "UTC"
    Europe_Moscow = "Europe/Moscow", "Москва"
    Asia_Yekaterinburg = "Asia/Yekaterinburg", "Екатеринбург"


class Profile(models.Model):
    """ Профиль """
    class Meta:
        db_table = "resources_profile"
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    """ Автогенерация """
    api_secret = models.CharField(verbose_name="API ключ", db_index=True)

    """ Настройки """
    can_notify_at_start = models.TimeField(blank=True, default=datetime.time(9, 00), null=True, verbose_name="можно оповещать с")
    can_notify_at_end = models.TimeField(blank=True, default=datetime.time(17, 00), null=True, verbose_name="можно оповещать до")
    can_notify_negative_portrate = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о сообщениях в Портрет")
    can_notify_negative_yandex = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в Яндекс Карты")
    can_notify_negative_gis = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в 2Гис Карты")
    can_notify_negative_google = models.BooleanField(default=True, verbose_name="получать оповещения в Telegram о негативных отзывах в Google Maps")
    default_timezone = models.CharField(blank=False, null=False, choices=Timezone.choices, default=Timezone.UTC, verbose_name="Временная зона по умолчанию")
    telegram_id = models.CharField(blank=True, null=True, verbose_name="telegram ID")

    """ Связи """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_init, sender=Profile)
def profile_post_init(sender, instance, **kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


class Company(models.Model):
    """ Компания """
    class Meta:
        db_table = "resources_company"
        verbose_name = "компания"
        verbose_name_plural = "компании"

    """ Автогенерация """
    api_secret = models.CharField(verbose_name="API ключ", db_index=True)

    """ Настройки """
    is_active = models.BooleanField(default=False, verbose_name="активно?")
    is_first_parsing = models.BooleanField(default=True, verbose_name="первый парсинг?")
    is_parse_yandex = models.BooleanField(default=False, verbose_name="парсить Яндекс?")
    is_parse_gis = models.BooleanField(default=False, verbose_name="парсить 2Гис?")
    is_parse_google = models.BooleanField(default=False, verbose_name="парсить Google?")

    """ Ссылки для парсеров """
    parser_link_yandex = models.CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    parser_link_gis = models.CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    parser_link_google = models.CharField(blank=True, null=True, verbose_name="ссылка Google")

    """ Контент """
    address = models.CharField(verbose_name="адрес")
    logo = models.ImageField(blank=True, null=True, upload_to="company_logo/%Y/%m/%d/", verbose_name="логотип")
    name = models.CharField(verbose_name="название")

    """ Форма запроса отзыва """
    form_link_yandex = models.CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    form_link_gis = models.CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    form_link_google = models.CharField(blank=True, null=True, verbose_name="ссылка Google")
    form_link_mapsme = models.CharField(blank=True, null=True, verbose_name="ссылка Mapsme")
    form_link_dikidi = models.CharField(blank=True, null=True, verbose_name="ссылка Dikidi")
    form_link_restoclub = models.CharField(blank=True, null=True, verbose_name="ссылка Рестоклуб")
    form_link_tripadvisor = models.CharField(blank=True, null=True, verbose_name="ссылка Tripadvisor")
    form_link_prodoctorov = models.CharField(blank=True, null=True, verbose_name="ссылка Продокторов")
    form_link_flamp = models.CharField(blank=True, null=True, verbose_name="ссылка Flamp")
    form_link_zoon = models.CharField(blank=True, null=True, verbose_name="ссылка Zoon")
    form_link_otzovik = models.CharField(blank=True, null=True, verbose_name="ссылка Отзовик")
    form_link_irecommend = models.CharField(blank=True, null=True, verbose_name="ссылка Irecommend")

    """ Связи """
    users = models.ManyToManyField(User, blank=True, verbose_name="пользователи")

    """ Агрегация общее """
    rating = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="Общий рейтинг")
    reviews_positive_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов")
    reviews_negative_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов")
    reviews_total_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов")
    messages_total_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество сообщений")

    """ Агрегация Яндекс """
    rating_yandex = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Яндекс")
    rating_yandex_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга Яндекс")
    reviews_yandex_positive_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс")
    reviews_yandex_negative_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс")
    reviews_yandex_total_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс")
    reviews_yandex_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов Яндекс")

    """ Агрегация 2Гис """
    rating_gis = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг 2Гис")
    rating_gis_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга 2Гис")
    reviews_gis_positive_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис")
    reviews_gis_negative_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис")
    reviews_gis_total_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис")
    reviews_gis_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов 2Гис")

    """ Агрегация Google """
    rating_google = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Google")
    rating_google_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга Google")
    reviews_google_positive_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google")
    reviews_google_negative_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google")
    reviews_google_total_count = models.IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google")
    reviews_google_last_parse_at = models.DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов Google")

    @property
    def form_tags(self):
        return ["Нагрубили", "Сделали не то", "Цена", "Плохое качество", "Долго"]

    @property
    def stars_svg(self):
        return f"images/stars/{self.rating}.svg"

    def __str__(self):
        return self.name


@receiver(post_init, sender=Company)
def company_post_init(sender, instance, **kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


class RatingStamp(models.Model):
    """ Рейтинг """
    class Meta:
        db_table = "resources_company_rating_stamp"
        verbose_name = "Рейтинг компании"
        verbose_name_plural = "Рейтинги компании"
        unique_together = ["company", "created_at"]

    """ Автогенерация """
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    rating_yandex = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Яндекс")
    rating_gis = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг 2Гис")
    rating_google = models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Google")

    """ Связи """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="компания")


class Review(models.Model):
    """ Отзыв """
    class Meta:
        db_table = "resources_review"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        unique_together = ["company", "remote_id"]

    """ Автогенерация """
    created_at = models.DateField(verbose_name="дата создания")

    """ Настройки """
    is_visible = models.BooleanField(verbose_name="отображается в виджете", default=True)
    remote_id = models.CharField(blank=True, null=True, verbose_name="ID (агрегация)")
    service = models.CharField(choices=Service.choices, default=Service.YANDEX, verbose_name="сервис")
    stars = models.IntegerField(blank=True, null=True, verbose_name="количество звезд")

    """ Контент """
    name = models.CharField(blank=True, null=True, verbose_name="пользователь")
    text = models.TextField(blank=True, null=True, verbose_name="текст отзыва")

    """ Связи """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="компания")

    @property
    def stars_svg(self):
        return f"images/stars/{float(self.stars)}.svg"

    @property
    def notification_template(self):
        return f"""📍 Негативный отзыв в {self.get_service_display()}

🏪 Компания:
{self.company}

📜 Текст:
{self.text}"""

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    from resources.tasks import send_telegram_text_task

    if created and not instance.company.is_first_parsing and instance.stars < 4:
        for user in instance.company.users.exclude(profile__telegram_id=None).all():
            if instance.service == Service.YANDEX and user.profile.can_notify_negative_yandex:
                send_telegram_text_task.delay(user.profile.telegram_id, instance.notification_template)

            elif instance.service == Service.GIS and user.profile.can_notify_negative_gis:
                send_telegram_text_task.delay(user.profile.telegram_id, instance.notification_template)

            elif instance.service == Service.GOOGLE and user.profile.can_notify_negative_google:
                send_telegram_text_task.delay(user.profile.telegram_id, instance.notification_template)


class Message(models.Model):
    """ Сообщение """
    class Meta:
        db_table = "resources_negative_message"
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    """ Автогенерация """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    phone = models.CharField(verbose_name="контактный телефон")
    text = models.TextField(blank=True, null=True, verbose_name="текст сообщения")

    """ Связи """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="компания")

    @property
    def notification_template(self):
        return f"""📍 Негативный отзыв в Портрете

🏪 Компания:
{self.company}

📱 Телефон:
{self.phone}

📜 Текст:
{self.text}"""

    def __str__(self):
        return self.phone


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    from resources.tasks import send_telegram_text_task

    if created:
        for user in instance.company.users.exclude(profile__telegram_id=None).all():
            if user.profile.can_notify_negative_portrate:
                send_telegram_text_task.delay(user.profile.telegram_id, instance.notification_template)
