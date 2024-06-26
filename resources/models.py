import asyncio
from datetime import time

from celery import chain
from django.conf import settings
from django.core.files import File
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    FileField,
    ForeignKey,
    DecimalField,
    DateTimeField,
    DateField,
    ManyToManyField,
    Model,
    OneToOneField,
    IntegerField,
    TextChoices,
    TextField,
    TimeField,
)
from django.db.models.signals import post_init
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.formats import localize
from django_resized import ResizedImageField
from djmoney.models.fields import MoneyField
from telegram import Bot

from pdf.utils import make_stick


class Service(TextChoices):
    """ Сервис """
    YANDEX = "YANDEX", "Яндекс"
    GIS = "GIS", "2Гис"
    GOOGLE = "GOOGLE", "Google"


class Stars(TextChoices):
    """ Звезды """
    _0 = "0", "Без оценки"
    _1 = "1", "★"
    _2 = "2", "★ ★"
    _3 = "3", "★ ★ ★"
    _4 = "4", "★ ★ ★ ★"
    _5 = "5", "★ ★ ★ ★ ★"


class Timezone(TextChoices):
    """ Часовой пояс """
    UTC = "UTC", "UTC"
    Europe_Moscow = "Europe/Moscow", "Москва"
    Asia_Yekaterinburg = "Asia/Yekaterinburg", "Екатеринбург"


class Rate(TextChoices):
    """ Часовой пояс """
    START = "STARTS", "Старт"
    REGULAR = "REGULAR", "Стандарт"
    BUSINESS = "BUSINESS", "Бизнес"


class Profile(Model):
    """ Профиль """
    class Meta:
        db_table = "resources_profile"
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    """ Автогенерация """
    api_secret = CharField(verbose_name="API ключ", db_index=True)
    balance = MoneyField(default=0, default_currency='RUB', decimal_places=2,  max_digits=14)
    is_billing = BooleanField(default=False, verbose_name="списывать оплату?")

    """ Настройки """
    default_timezone = CharField(blank=False, null=False, choices=Timezone.choices, default=Timezone.UTC, verbose_name="Временная зона по умолчанию")
    telegram_id = CharField(blank=True, null=True, verbose_name="telegram ID")
    rate = CharField(blank=False, null=False, choices=Rate.choices, default=Rate.START, verbose_name="Тариф")

    """ Связи """
    user = OneToOneField("auth.User", on_delete=CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_init, sender=Profile)
def profile_post_init(sender, instance, **kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


class Company(Model):
    """ Компания """
    class Meta:
        db_table = "resources_company"
        verbose_name = "компания"
        verbose_name_plural = "компании"

    """ Автогенерация """
    api_secret = CharField(verbose_name="API ключ", db_index=True)

    """ Настройки """
    is_first_parsing = BooleanField(default=True, verbose_name="первый парсинг?")
    is_parse_yandex = BooleanField(default=False, verbose_name="парсить Яндекс?")
    is_parse_gis = BooleanField(default=False, verbose_name="парсить 2Гис?")
    is_parse_google = BooleanField(default=False, verbose_name="парсить Google?")

    """ Ссылки для парсеров """
    parser_link_yandex = CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    parser_link_gis = CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    parser_link_google = CharField(blank=True, null=True, verbose_name="ссылка Google")

    """ Контент """
    address = CharField(blank=True, null=True, verbose_name="адрес")
    logo = ResizedImageField(blank=True, crop=['middle', 'center'], null=True, size=[300, 300], upload_to="dashboard/%Y/%m/%d/", verbose_name="логотип")
    name = CharField(verbose_name="название")
    phone = CharField(blank=True, null=True, verbose_name="телефон")

    """ QR """
    business_light = FileField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="визитка темная тема")
    business_dark = FileField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="визитка темная тема")
    stick_light = FileField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="наклейка светлая тема")
    stick_dark = FileField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="наклейка темная тема")

    """ Форма запроса отзыва """
    form_link_yandex = CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    form_link_gis = CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    form_link_google = CharField(blank=True, null=True, verbose_name="ссылка Google")
    form_link_dikidi = CharField(blank=True, null=True, verbose_name="ссылка Dikidi")
    form_link_restoclub = CharField(blank=True, null=True, verbose_name="ссылка Рестоклуб")
    form_link_tripadvisor = CharField(blank=True, null=True, verbose_name="ссылка Tripadvisor")
    form_link_prodoctorov = CharField(blank=True, null=True, verbose_name="ссылка Продокторов")
    form_link_flamp = CharField(blank=True, null=True, verbose_name="ссылка Flamp")
    form_link_zoon = CharField(blank=True, null=True, verbose_name="ссылка Zoon")
    form_link_otzovik = CharField(blank=True, null=True, verbose_name="ссылка Отзовик")
    form_link_irecommend = CharField(blank=True, null=True, verbose_name="ссылка Irecommend")

    """ Контакты """
    form_contact_whatsapp = CharField(blank=True, null=True, verbose_name="ссылка Whatsapp")
    form_contact_telegram = CharField(blank=True, null=True, verbose_name="ссылка Telegram")
    form_contact_viber = CharField(blank=True, null=True, verbose_name="ссылка Viber")
    form_contact_website = CharField(blank=True, null=True, verbose_name="ссылка Вебсайт")
    form_contact_vk = CharField(blank=True, null=True, verbose_name="ссылка VK")
    form_contact_ok = CharField(blank=True, null=True, verbose_name="ссылка Одноклассники")
    form_contact_facebook = CharField(blank=True, null=True, verbose_name="ссылка Facebook")
    form_contact_instagram = CharField(blank=True, null=True, verbose_name="ссылка Instagram")
    form_contact_youtube = CharField(blank=True, null=True, verbose_name="ссылка Youtube")
    form_contact_x = CharField(blank=True, null=True, verbose_name="ссылка X")

    """ Агрегация общее """
    rating = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name="Общий рейтинг")
    reviews_positive_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов")
    reviews_negative_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов")
    reviews_total_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов")
    messages_total_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество сообщений")

    """ Агрегация Яндекс """
    rating_yandex = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Яндекс")
    rating_yandex_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга Яндекс")
    #
    reviews_yandex_positive_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс")
    reviews_yandex_positive_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс за неделю")
    reviews_yandex_positive_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс за месяц")
    reviews_yandex_positive_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс за квартал")
    reviews_yandex_positive_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Яндекс за год")
    #
    reviews_yandex_negative_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс")
    reviews_yandex_negative_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс за неделю")
    reviews_yandex_negative_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс за месяц")
    reviews_yandex_negative_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс за квартал")
    reviews_yandex_negative_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Яндекс за год")
    #
    reviews_yandex_total_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс")
    reviews_yandex_total_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс за неделю")
    reviews_yandex_total_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс за месяц")
    reviews_yandex_total_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс за квартал")
    reviews_yandex_total_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Яндекс за год")
    #
    reviews_yandex_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов Яндекс")

    """ Агрегация 2Гис """
    rating_gis = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг 2Гис")
    rating_gis_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга 2Гис")
    #
    reviews_gis_positive_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис")
    reviews_gis_positive_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис за неделю")
    reviews_gis_positive_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис за месяц")
    reviews_gis_positive_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис за квартал")
    reviews_gis_positive_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов 2Гис за год")
    #
    reviews_gis_negative_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис")
    reviews_gis_negative_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис за неделю")
    reviews_gis_negative_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис за месяц")
    reviews_gis_negative_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис за квартал")
    reviews_gis_negative_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов 2Гис за год")
    #
    reviews_gis_total_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис")
    reviews_gis_total_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис за неделю")
    reviews_gis_total_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис за месяц")
    reviews_gis_total_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис за квартал")
    reviews_gis_total_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов 2Гис за год")
    #
    reviews_gis_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов 2Гис")

    """ Агрегация Google """
    rating_google = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Google")
    rating_google_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки рейтинга Google")
    #
    reviews_google_positive_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google")
    reviews_google_positive_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google за неделю")
    reviews_google_positive_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google за месяц")
    reviews_google_positive_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google за квартал")
    reviews_google_positive_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество позитивных отзывов Google за год")
    #
    reviews_google_negative_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google")
    reviews_google_negative_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google за неделю")
    reviews_google_negative_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google за месяц")
    reviews_google_negative_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google за квартал")
    reviews_google_negative_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество негативных отзывов Google за год")
    #
    reviews_google_total_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google")
    reviews_google_total_week_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google за неделю")
    reviews_google_total_month_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google за месяц")
    reviews_google_total_quarter_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google за квартал")
    reviews_google_total_year_count = IntegerField(blank=True, default=0, null=True, verbose_name="количество отзывов Google за год")
    #
    reviews_google_last_parse_at = DateTimeField(blank=True, null=True, verbose_name="дата последней загрузки отзывов Google")

    """ Связи """
    users = ManyToManyField("auth.User", blank=True, verbose_name="пользователи", through="resources.Membership")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_parser_link_yandex = self.parser_link_yandex
        self.cached_parser_link_gis = self.parser_link_gis
        self.cached_parser_link_google = self.parser_link_google

    @property
    def form_tags(self):
        return ["Нагрубили", "Сделали не то", "Цена", "Плохое качество", "Долго"]

    @property
    def stars_svg_yandex(self):
        return f"images/stars/{self.rating_yandex}.svg"

    @property
    def stars_svg_gis(self):
        return f"images/stars/{self.rating_gis}.svg"

    def stars_svg_google(self):
        return f"images/stars/{self.rating_google}.svg"

    @property
    def stars_svg(self):
        return f"images/stars/{self.rating}.svg"

    @property
    def has_contacts(self):
        if (
                self.form_contact_whatsapp or
                self.form_contact_telegram or
                self.form_contact_viber or
                self.form_contact_website or
                self.form_contact_vk or
                self.form_contact_ok or
                self.form_contact_facebook or
                self.form_contact_instagram or
                self.form_contact_youtube or
                self.form_contact_x

        ):
            return True
        else:
            return False

    def __str__(self):
        return self.name


@receiver(post_init, sender=Company)
def company_post_init(sender, instance, **kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


@receiver(post_save, sender=Company)
def company_post_save(sender, instance, created, **kwargs):
    if created:
        instance.stick_light.save("stick_light.pdf", File(make_stick(instance.id, "light")))
        instance.stick_dark.save("stick_dark.pdf", File(make_stick(instance.id, "dark")))

    if not created:
        # @TODO сделать очистку существующих отзывов если ссылку поменяли
        # if instance.cached_parser_link_yandex != instance.parser_link_yandex:
        # if instance.cached_parser_link_gis != instance.parser_link_gis:
        # if instance.cached_parser_link_google != instance.parser_link_google:
        pass


class Membership(Model):
    """ Личная настройка для компании """
    class Meta:
        db_table = "resources_membership"
        verbose_name = "участник"
        verbose_name_plural = "участники"

    """ Настройки """
    can_notify_negative_portrate = BooleanField(default=True, verbose_name="оповещения Портрет")
    can_notify_negative_yandex = BooleanField(default=True, verbose_name="оповещения Яндекс")
    can_notify_negative_gis = BooleanField(default=True, verbose_name="оповещения 2Гис")
    can_notify_negative_google = BooleanField(default=True, verbose_name="оповещения Google")
    can_notify_at_start = TimeField(blank=True, default=time(9, 00), null=True, verbose_name="можно оповещать с")
    can_notify_at_end = TimeField(blank=True, default=time(17, 00), null=True, verbose_name="можно оповещать до")
    can_notify_at_from_stars = IntegerField(blank=True, default=3, null=True, verbose_name="количество звезд для оповещений")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE)
    user = ForeignKey("auth.User", on_delete=CASCADE)

    def __str__(self):
        return f"{self.company}-{self.user}"


class RatingStamp(Model):
    """ Рейтинг """
    class Meta:
        db_table = "resources_company_rating_stamp"
        verbose_name = "Рейтинг компании"
        verbose_name_plural = "Рейтинги компании"
        unique_together = ["company", "created_at"]

    """ Автогенерация """
    created_at = DateField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    rating_yandex = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Яндекс")
    rating_gis = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг 2Гис")
    rating_google = DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True,verbose_name="рейтинг Google")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="компания")

    def __str__(self):
        return f"{self.company}-{self.created_at}"


class Review(Model):
    """ Отзыв """
    class Meta:
        db_table = "resources_review"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        unique_together = ["company", "remote_id"]

    """ Автогенерация """
    created_at = DateField(verbose_name="дата создания")

    """ Настройки """
    is_visible = BooleanField(verbose_name="отображается в виджете", default=True)
    remote_id = CharField(verbose_name="ID (агрегация)")
    service = CharField(choices=Service.choices, default=Service.YANDEX, verbose_name="сервис")
    stars = IntegerField(default=0, verbose_name="количество звезд")

    """ Контент """
    name = CharField(verbose_name="пользователь")
    text = TextField(verbose_name="текст отзыва")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="компания")

    @property
    def parser_png(self):
        return f"images/parsers/{self.service.lower()}.png"

    @property
    def stars_svg(self):
        return f"images/stars/{float(self.stars)}.svg"

    @property
    def stars_text(self):
        return self.stars * '★ '

    @property
    def text_length(self):
        return len(self.text)

    @property
    def notification_template(self):
        return f"""Новый отзыв в {self.get_service_display()}

📍 Филиал:
{self.company}

📅 Дата публикации:
{localize(self.created_at)}

📊 Оценка:
{self.stars_text}

💬 Текст:
{self.text}"""

    def __str__(self):
        return self.name


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    if created and not instance.company.is_first_parsing:
        for user in instance.company.users.filter(**{f"membership__can_notify_negative_{instance.service.lower()}": True}).exclude(profile__telegram_id=None).all():
            asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(user.profile.telegram_id, instance.notification_template))


class Message(Model):
    """ Сообщение """
    class Meta:
        db_table = "resources_negative_message"
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    """ Автогенерация """
    created_at = DateTimeField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    phone = CharField(verbose_name="контактный телефон")
    text = TextField(blank=True, null=True, verbose_name="текст сообщения")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="компания")

    @property
    def notification_template(self):
        return f"""Негативный отзыв в Портрете

📍 Филиал:
{self.company}

📅 Дата публикации:
{localize(self.created_at)}

💬 Текст:
{self.text}

📱 Телефон:
{self.phone}"""

    def __str__(self):
        return self.phone


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        for user in instance.company.users.filter(membership__can_notify_negative_portrate=True).exclude(profile__telegram_id=None).all():
            asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(user.profile.telegram_id, instance.notification_template))
