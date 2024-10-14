import asyncio
import math
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    DecimalField,
    DateTimeField,
    DateField,
    IntegerField,
    ManyToManyField,
    Model,
    Manager,
    Prefetch,
    OneToOneField,
    TextChoices,
    TextField, FileField, ImageField
)
from django.db.models.signals import post_init
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.formats import localize
from django_resized import ResizedImageField
from djmoney.models.fields import MoneyField
from telegram import Bot


class Period(TextChoices):
    """ Период оплаты """
    ANNUALLY = "ANNUALLY", "Год"
    MONTHLY = "MONTHLY", "Месяц"


class Rate(TextChoices):
    """ Тариф """
    START = "START", "Старт"
    REGULAR = "REGULAR", "Стандарт"
    BUSINESS = "BUSINESS", "Бизнес"


class Service(TextChoices):
    """ Сервис """
    PORTRATE = "PORTRATE", "Портрет"
    YANDEX = "YANDEX", "Яндекс"
    GIS = "GIS", "2Гис"
    GOOGLE = "GOOGLE", "Google"
    AVITO = "AVITO", "Авито"
    ZOON = "ZOON", "Zoon"
    FLAMP = "FLAMP", "Flamp"
    YELL = "YELL", "Yell"    
    PRODOCTOROV = "PRODOCTOROV", "Продокторов"
    YANDEX_SERVICES = "YANDEX_SERVICES", "Яндекс Услуги"
    OTZOVIK = "OTZOVIK", "Otzovik"
    IRECOMMEND = "IRECOMMEND", "Irecommend"
    TRIPADVISOR = "TRIPADVISOR", "Tripadvisor"


class Stars(TextChoices):
    """ Звезды """
    _0 = "0", "0.0"
    _1 = "1", "1.0"
    _2 = "2", "2.0"
    _3 = "3", "3.0"
    _4 = "4", "4.0"
    _5 = "5", "5.0"


class Timezone(TextChoices):
    """ Часовой пояс """
    UTC = "UTC", "UTC"
    Europe_Moscow = "Europe/Moscow", "Москва"
    Asia_Yekaterinburg = "Asia/Yekaterinburg", "Екатеринбург"


class ClickStamp(Model):
    """ Отпечаток клика по кнопке сервиса на форме запроса отзывов """
    class Meta:
        db_table = "resources_click_stamp"
        verbose_name = "Отпечаток клика по кнопке сервиса на форме запроса отзывов"
        verbose_name_plural = "Отпечатки клика по кнопке сервиса на форме запроса отзывов"

    """ Автогенерация """
    created_at = DateField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    service = CharField(choices=Service.choices, default=Service.YANDEX, verbose_name="сервис")

    """ Связи """
    visit_stamp = ForeignKey("resources.VisitStamp", on_delete=CASCADE, verbose_name="отпечаток перехода на форму запроса отзывов")
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="филиал")

    def __str__(self):
        return f"{self.company} → {self.service} - {self.created_at}"


class CompanyManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                "users",
                to_attr="users_is_owner",
                queryset=User.objects.filter(membership__is_owner=True).select_related("profile")
            )
        )


class Company(Model):
    """ Филиал """
    class Meta:
        db_table = "resources_company"
        verbose_name = "филиал"
        verbose_name_plural = "филиалы"

    objects = CompanyManager()

    """ Автогенерация """
    api_secret = CharField(blank=True, db_index=True, null=True, verbose_name="API ключ")

    """ Настройки """
    is_visible_0 = BooleanField(default=False, verbose_name="отображать с 0 звезд?")
    is_visible_1 = BooleanField(default=False, verbose_name="отображать с 1 звездой?")
    is_visible_2 = BooleanField(default=False, verbose_name="отображать с 2 звездами?")
    is_visible_3 = BooleanField(default=False, verbose_name="отображать с 3 звездами?")
    is_visible_4 = BooleanField(default=True, verbose_name="отображать с 4 звездами?")
    is_visible_5 = BooleanField(default=True, verbose_name="отображать с 5 звездами?")
    is_visible_portrate = BooleanField(default=True, verbose_name="отображать Портрет?")
    is_visible_yandex = BooleanField(default=True, verbose_name="отображать Яндекс?")
    is_visible_gis = BooleanField(default=True, verbose_name="отображать 2Гис?")
    is_visible_google = BooleanField(default=True, verbose_name="отображать Google?")
    is_visible_avito = BooleanField(default=True, verbose_name="отображать Авито?")
    is_visible_zoon = BooleanField(default=True, verbose_name="отображать Zoon?")
    is_visible_flamp = BooleanField(default=True, verbose_name="отображать Flamp?")
    is_visible_yell = BooleanField(default=True, verbose_name="отображать Yell?")
    is_visible_prodoctorov = BooleanField(default=True, verbose_name="отображать Продокторов?")
    is_visible_yandex_services = BooleanField(default=True, verbose_name="отображать Яндекс услуги?")
    is_visible_otzovik = BooleanField(default=True, verbose_name="отображать Otzovik?")
    is_visible_irecommend = BooleanField(default=True, verbose_name="отображать Irecommend?")
    is_visible_tripadvisor = BooleanField(default=True, verbose_name="отображать Tripadvisor?")
    is_visible_short = BooleanField(default=False, verbose_name="отображать короткие?")

    """ Парсер Яндекса """
    is_first_parsing_yandex = BooleanField(default=True, verbose_name="это первый парсинг Яндекс?")
    is_parser_run_yandex = BooleanField(default=False, verbose_name="парсер Яндекс сейчас запущен?")
    parser_link_yandex = CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    parser_last_change_at_yandex = DateField(blank=True, null=True, verbose_name="дата последнего изменения Яндекс")
    parser_last_parse_at_yandex = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Яндекс")

    """ Парсер 2Гис """
    is_first_parsing_gis = BooleanField(default=True, verbose_name="это первый парсинг 2Гис?")
    is_parser_run_gis = BooleanField(default=False, verbose_name="парсер 2Гис сейчас запущен?")
    parser_link_gis = CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    parser_last_change_at_gis = DateField(blank=True, null=True, verbose_name="дата последнего изменения 2Гис")
    parser_last_parse_at_gis = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки 2Гис")

    """ Парсер Google """
    is_first_parsing_google = BooleanField(default=True, verbose_name="это первый парсинг Google?")
    is_parser_run_google = BooleanField(default=False, verbose_name="парсер Google сейчас запущен?")
    parser_link_google = CharField(blank=True, null=True, verbose_name="ссылка Google")
    parser_last_change_at_google = DateField(blank=True, null=True, verbose_name="дата последнего изменения Google")
    parser_last_parse_at_google = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Google")

    """ Парсер Avito """
    is_first_parsing_avito = BooleanField(default=True, verbose_name="это первый парсинг Авито?")
    is_parser_run_avito = BooleanField(default=False, verbose_name="парсер Авито сейчас запущен?")
    parser_link_avito = CharField(blank=True, null=True, verbose_name="ссылка Авито")
    parser_last_change_at_avito = DateField(blank=True, null=True, verbose_name="дата последнего изменения Авито")
    parser_last_parse_at_avito = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Авито")

    """ Парсер Zoon """
    is_first_parsing_zoon = BooleanField(default=True, verbose_name="это первый парсинг Zoon?")
    is_parser_run_zoon = BooleanField(default=False, verbose_name="парсер Zoon сейчас запущен?")
    parser_link_zoon = CharField(blank=True, null=True, verbose_name="ссылка Zoon")
    parser_last_change_at_zoon = DateField(blank=True, null=True, verbose_name="дата последнего изменения Zoon")
    parser_last_parse_at_zoon = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Zoon")

    """ Парсер Flamp """
    is_first_parsing_flamp = BooleanField(default=True, verbose_name="это первый парсинг Flamp?")
    is_parser_run_flamp = BooleanField(default=False, verbose_name="парсер Flamp сейчас запущен?")
    parser_link_flamp = CharField(blank=True, null=True, verbose_name="ссылка Flamp")
    parser_last_change_at_flamp = DateField(blank=True, null=True, verbose_name="дата последнего изменения Flamp")
    parser_last_parse_at_flamp = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Flamp")

    """ Парсер Yell """
    is_first_parsing_yell = BooleanField(default=True, verbose_name="это первый парсинг Yell?")
    is_parser_run_yell = BooleanField(default=False, verbose_name="парсер Yell сейчас запущен?")
    parser_link_yell = CharField(blank=True, null=True, verbose_name="ссылка Yell")
    parser_last_change_at_yell = DateField(blank=True, null=True, verbose_name="дата последнего изменения Yell")
    parser_last_parse_at_yell = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Yell")

    """ Парсер Продокторов """
    is_first_parsing_prodoctorov= BooleanField(default=True, verbose_name="это первый парсинг Продокторов?")
    is_parser_run_prodoctorov = BooleanField(default=False, verbose_name="парсер Продокторов сейчас запущен?")
    parser_link_prodoctorov = CharField(blank=True, null=True, verbose_name="ссылка Продокторов")
    parser_last_change_at_prodoctorov = DateField(blank=True, null=True, verbose_name="дата последнего изменения Продокторов")
    parser_last_parse_at_prodoctorov = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Продокторов")

    """ Парсер Яндекс Сервисы """
    is_first_parsing_yandex_services = BooleanField(default=True, verbose_name="это первый парсинг Яндекс Сервисы?")
    is_parser_run_yandex_services = BooleanField(default=False, verbose_name="парсер Яндекс Сервисы сейчас запущен?")
    parser_link_yandex_services = CharField(blank=True, null=True, verbose_name="ссылка Яндекс Сервисы")
    parser_last_change_at_yandex_services = DateField(blank=True, null=True, verbose_name="дата последнего изменения Яндекс Сервисы")
    parser_last_parse_at_yandex_services = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Яндекс Сервисы")

    """ Парсер Отзовик """
    is_first_parsing_otzovik = BooleanField(default=True, verbose_name="это первый парсинг Отзовик?")
    is_parser_run_otzovik = BooleanField(default=False, verbose_name="парсер Отзовик сейчас запущен?")
    parser_link_otzovik = CharField(blank=True, null=True, verbose_name="ссылка Отзовик")
    parser_last_change_at_otzovik = DateField(blank=True, null=True, verbose_name="дата последнего изменения Отзовик")
    parser_last_parse_at_otzovik = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Отзовик")

    """ Парсер Irecommend """
    is_first_parsing_irecommend = BooleanField(default=True, verbose_name="это первый парсинг Irecommend?")
    is_parser_run_irecommend = BooleanField(default=False, verbose_name="парсер Irecommend сейчас запущен?")
    parser_link_irecommend = CharField(blank=True, null=True, verbose_name="ссылка Irecommend")
    parser_last_change_at_irecommend = DateField(blank=True, null=True, verbose_name="дата последнего изменения Irecommend")
    parser_last_parse_at_irecommend = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Irecommend")

    """ Парсер Tripadvisor """
    is_first_parsing_tripadvisor = BooleanField(default=True, verbose_name="это первый парсинг Tripadvisor?")
    is_parser_run_tripadvisor = BooleanField(default=False, verbose_name="парсер Tripadvisor сейчас запущен?")
    parser_link_tripadvisor = CharField(blank=True, null=True, verbose_name="ссылка Tripadvisor")
    parser_last_change_at_tripadvisor = DateField(blank=True, null=True, verbose_name="дата последнего изменения Tripadvisor")
    parser_last_parse_at_tripadvisor = DateTimeField(blank=True, null=True, verbose_name="дата и время последней загрузки Tripadvisor")

    """ Контент """
    address = CharField(blank=True, null=True, verbose_name="адрес")
    logo = ResizedImageField(blank=True, crop=['middle', 'center'], null=True, size=[300, 300], upload_to="dashboard/%Y/%m/%d/", verbose_name="логотип")
    name = CharField(verbose_name="название")
    phone = CharField(blank=True, null=True, verbose_name="телефон")

    feedback_link_yandex = CharField(blank=True, null=True, verbose_name="ссылка Яндекс")
    feedback_link_gis = CharField(blank=True, null=True, verbose_name="ссылка 2Гис")
    feedback_link_google = CharField(blank=True, null=True, verbose_name="ссылка Google")
    feedback_link_avito = CharField(blank=True, null=True, verbose_name="ссылка Авито")
    feedback_link_zoon = CharField(blank=True, null=True, verbose_name="ссылка Zoon")
    feedback_link_flamp = CharField(blank=True, null=True, verbose_name="ссылка Flamp")
    feedback_link_yell = CharField(blank=True, null=True, verbose_name="ссылка Yell")
    feedback_link_prodoctorov = CharField(blank=True, null=True, verbose_name="ссылка Продокторов")
    feedback_link_yandex_services = CharField(blank=True, null=True, verbose_name="ссылка Яндекс услуги")
    feedback_link_otzovik = CharField(blank=True, null=True, verbose_name="ссылка Отзовик")
    feedback_link_irecommend = CharField(blank=True, null=True, verbose_name="ссылка Irecommend")
    feedback_link_tripadvisor = CharField(blank=True, null=True, verbose_name="ссылка Tripadvisor")

    feedback_contact_whatsapp = CharField(blank=True, null=True, verbose_name="ссылка Whatsapp")
    feedback_contact_telegram = CharField(blank=True, null=True, verbose_name="ссылка Telegram")
    feedback_contact_viber = CharField(blank=True, null=True, verbose_name="ссылка Viber")
    feedback_contact_website = CharField(blank=True, null=True, verbose_name="ссылка Вебсайт")
    feedback_contact_vk = CharField(blank=True, null=True, verbose_name="ссылка VK")
    feedback_contact_ok = CharField(blank=True, null=True, verbose_name="ссылка Одноклассники")
    feedback_contact_facebook = CharField(blank=True, null=True, verbose_name="ссылка Facebook")
    feedback_contact_instagram = CharField(blank=True, null=True, verbose_name="ссылка Instagram")
    feedback_contact_x = CharField(blank=True, null=True, verbose_name="ссылка X")
    feedback_contact_youtube = CharField(blank=True, null=True, verbose_name="ссылка Youtube")
    feedback_contact_rutube = CharField(blank=True, null=True, verbose_name="ссылка Rutube")
    feedback_contact_vimeo = CharField(blank=True, null=True, verbose_name="ссылка Vimeo")

    feedback_text_rate_heading = CharField(default="Вам понравилось обслуживание?", verbose_name="заголовок главной страницы")
    feedback_text_request_heading = CharField(default="Наградите нас отзывом", verbose_name="заголовок страницы запроса отзывов")
    feedback_text_create_heading = CharField(default="Написать директору", verbose_name="заголовок страницы создания жалобы")
    feedback_text_success_heading = CharField(default="Ваше сообщение отправлено", verbose_name="заголовок страницы после оставления жалобы")
    feedback_text_success_text = CharField(default="Спасибо за обращение, в близжайшее время с вами свяжется наш администратор по указанному вам телефону.", verbose_name="текст страницы после оставления жалобы")

    """ Агрегация """
    rating_yandex = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Яндекс")
    rating_gis = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг 2Гис")
    rating_google = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Google")
    rating_avito = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Авито")
    rating_zoon = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Zoon")
    rating_flamp = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Flamp")
    rating_yell = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Yell")
    rating_prodoctorov = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Продокторов")
    rating_yandex_services = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Яндекс услуги")
    rating_otzovik = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Отзовик")
    rating_irecommend = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Irecommend")
    rating_tripadvisor = DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name="рейтинг Tripadvisor")

    reviews_count_remote_yandex = IntegerField(default=0, verbose_name="количество отзывов Яндекс")
    reviews_count_remote_gis = IntegerField(default=0, verbose_name="количество отзывов 2Гис")
    reviews_count_remote_google = IntegerField(default=0, verbose_name="количество отзывов Google")
    reviews_count_remote_avito = IntegerField(default=0, verbose_name="количество отзывов Авито")
    reviews_count_remote_zoon = IntegerField(default=0, verbose_name="количество отзывов Zoon")
    reviews_count_remote_flamp = IntegerField(default=0, verbose_name="количество отзывов Flamp")
    reviews_count_remote_yell = IntegerField(default=0, verbose_name="количество отзывов Yell")
    reviews_count_remote_prodoctorov = IntegerField(default=0, verbose_name="количество отзывов Продокторов")
    reviews_count_remote_yandex_services = IntegerField(default=0, verbose_name="количество отзывов Яндекс услуги")
    reviews_count_remote_otzovik = IntegerField(default=0, verbose_name="количество отзывов Отзовик")
    reviews_count_remote_irecommend = IntegerField(default=0, verbose_name="количество отзывов Irecommend")
    reviews_count_remote_tripadvisor = IntegerField(default=0, verbose_name="количество отзывов Tripadvisor")

    """ Связи """
    users = ManyToManyField("auth.User", verbose_name="пользователи", through="resources.Membership")

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, ** kwargs)
        self.cached_parser_link_yandex = self.parser_link_yandex
        self.cached_parser_link_gis = self.parser_link_gis
        self.cached_parser_link_google = self.parser_link_google
        self.cached_parser_link_avito = self.parser_link_avito
        self.cached_parser_link_zoon = self.parser_link_zoon
        self.cached_parser_link_flamp = self.parser_link_flamp
        self.cached_parser_link_yell = self.parser_link_yell
        self.cached_parser_link_prodoctorov = self.parser_link_prodoctorov
        self.cached_parser_link_yandex_services = self.parser_link_yandex_services
        self.cached_parser_link_otzovik = self.parser_link_otzovik
        self.cached_parser_link_irecommend = self.parser_link_irecommend
        self.cached_parser_link_tripadvisor = self.parser_link_tripadvisor

    def __str__(self):
        return str(self.name)

    @property
    def feedback_form_tags(self):
        return ["Нагрубили", "Сделали не то", "Цена", "Плохое качество", "Долго"]

    @property
    def feedback_utm_source_tags(self):
        return ["SMS", "Telegram", "Vk", "Whatsapp", "Instagram"]

    @property
    def has_contacts(self):
        if (
                self.feedback_contact_whatsapp or
                self.feedback_contact_telegram or
                self.feedback_contact_viber or
                self.feedback_contact_website or
                self.feedback_contact_vk or
                self.feedback_contact_ok or
                self.feedback_contact_facebook or
                self.feedback_contact_instagram or
                self.feedback_contact_x or
                self.feedback_contact_youtube or
                self.feedback_contact_rutube or
                self.feedback_contact_vimeo
        ):
            return True
        else:
            return False

    @property
    def is_active(self):
        try:
            return self.users_is_owner[0].profile.is_active
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_yandex(self):
        try:
            return self.users_is_owner[0].profile.can_parse_yandex
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_gis(self):
        try:
            return self.users_is_owner[0].profile.can_parse_gis
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_google(self):
        try:
            return self.users_is_owner[0].profile.can_parse_google
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_avito(self):
        try:
            return self.users_is_owner[0].profile.can_parse_avito
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_zoon(self):
        try:
            return self.users_is_owner[0].profile.can_parse_zoon
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_flamp(self):
        try:
            return self.users_is_owner[0].profile.can_parse_flamp
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_yell(self):
        try:
            return self.users_is_owner[0].profile.can_parse_yell
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_prodoctorov(self):
        try:
            return self.users_is_owner[0].profile.can_parse_prodoctorov
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_yandex_services(self):
        try:
            return self.users_is_owner[0].profile.can_parse_yandex_services
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_otzovik(self):
        try:
            return self.users_is_owner[0].profile.can_parse_otzovik
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_irecommend(self):
        try:
            return self.users_is_owner[0].profile.can_parse_irecommend
        except (AttributeError, IndexError):
            return False

    @property
    def can_parse_tripadvisor(self):
        try:
            return self.users_is_owner[0].profile.can_parse_tripadvisor
        except (AttributeError, IndexError):
            return False

    @property
    def is_parser_link_yandex_changed(self):
        return self.cached_parser_link_yandex != self.parser_link_yandex

    @property
    def is_parser_link_yandex_disabled(self):
        return self.parser_last_change_at_yandex == date.today()

    @property
    def is_parser_run_yandex_need(self):
        return self.parser_link_yandex and self.is_parser_link_yandex_changed

    @property
    def is_parser_link_gis_changed(self):
        return self.cached_parser_link_gis != self.parser_link_gis

    @property
    def is_parser_link_gis_disabled(self):
        return self.parser_last_change_at_gis == date.today()

    @property
    def is_parser_run_gis_need(self):
        return self.parser_link_gis and self.is_parser_link_gis_changed

    @property
    def is_parser_link_google_changed(self):
        return self.cached_parser_link_google != self.parser_link_google

    @property
    def is_parser_link_google_disabled(self):
        return self.parser_last_change_at_google == date.today()

    @property
    def is_parser_run_google_need(self):
        return self.parser_link_google and self.is_parser_link_google_changed

    @property
    def is_parser_link_avito_changed(self):
        return self.cached_parser_link_avito != self.parser_link_avito

    @property
    def is_parser_link_avito_disabled(self):
        return self.parser_last_change_at_avito == date.today()

    @property
    def is_parser_run_avito_need(self):
        return self.parser_link_avito and self.is_parser_link_avito_changed

    @property
    def is_parser_link_zoon_changed(self):
        return self.cached_parser_link_zoon != self.parser_link_zoon

    @property
    def is_parser_link_zoon_disabled(self):
        return self.parser_last_change_at_zoon == date.today()

    @property
    def is_parser_run_zoon_need(self):
        return self.parser_link_zoon and self.is_parser_link_zoon_changed

    @property
    def is_parser_link_flamp_changed(self):
        return self.cached_parser_link_flamp != self.parser_link_flamp

    @property
    def is_parser_link_flamp_disabled(self):
        return self.parser_last_change_at_flamp == date.today()

    @property
    def is_parser_run_flamp_need(self):
        return self.parser_link_flamp and self.is_parser_link_flamp_changed

    @property
    def is_parser_link_yell_changed(self):
        return self.cached_parser_link_yell != self.parser_link_yell

    @property
    def is_parser_link_yell_disabled(self):
        return self.parser_last_change_at_yell == date.today()

    @property
    def is_parser_run_yell_need(self):
        return self.parser_link_yell and self.is_parser_link_yell_changed

    @property
    def is_parser_link_prodoctorov_changed(self):
        return self.cached_parser_link_prodoctorov != self.parser_link_prodoctorov

    @property
    def is_parser_link_prodoctorov_disabled(self):
        return self.parser_last_change_at_prodoctorov == date.today()

    @property
    def is_parser_run_prodoctorov_need(self):
        return self.parser_link_prodoctorov and self.is_parser_link_prodoctorov_changed

    @property
    def is_parser_link_yandex_services_changed(self):
        return self.cached_parser_link_yandex_services != self.parser_link_yandex_services

    @property
    def is_parser_link_yandex_services_disabled(self):
        return self.parser_last_change_at_yandex_services == date.today()

    @property
    def is_parser_run_yandex_services_need(self):
        return self.parser_link_yandex_services and self.is_parser_link_yandex_services_changed

    @property
    def is_parser_link_otzovik_changed(self):
        return self.cached_parser_link_otzovik != self.parser_link_otzovik

    @property
    def is_parser_link_otzovik_disabled(self):
        return self.parser_last_change_at_otzovik == date.today()

    @property
    def is_parser_run_otzovik_need(self):
        return self.parser_link_otzovik and self.is_parser_link_otzovik_changed

    @property
    def is_parser_link_irecommend_changed(self):
        return self.cached_parser_link_irecommend != self.parser_link_irecommend

    @property
    def is_parser_link_irecommend_disabled(self):
        return self.parser_last_change_at_irecommend == date.today()

    @property
    def is_parser_run_irecommend_need(self):
        return self.parser_link_irecommend and self.is_parser_link_irecommend_changed

    @property
    def is_parser_link_tripadvisor_changed(self):
        return self.cached_parser_link_tripadvisor != self.parser_link_tripadvisor

    @property
    def is_parser_link_tripadvisor_disabled(self):
        return self.parser_last_change_at_tripadvisor == date.today()

    @property
    def is_parser_run_tripadvisor_need(self):
        return self.parser_link_tripadvisor and self.is_parser_link_tripadvisor_changed

    @property
    def rating_yandex_str(self):
        return str(self.rating_yandex)

    @property
    def rating_gis_str(self):
        return str(self.rating_gis)

    @property
    def rating_google_str(self):
        return str(self.rating_google)

    @property
    def rating_avito_str(self):
        return str(self.rating_avito)

    @property
    def rating_zoon_str(self):
        return str(self.rating_zoon)

    @property
    def rating_flamp_str(self):
        return str(self.rating_flamp)

    @property
    def rating_yell_str(self):
        return str(self.rating_yell)

    @property
    def rating_prodoctorov_str(self):
        return str(self.rating_prodoctorov)

    @property
    def rating_yandex_services_str(self):
        return str(self.rating_yandex_services)

    @property
    def rating_otzovik_str(self):
        return str(self.rating_otzovik)

    @property
    def rating_irecommend_str(self):
        return str(self.rating_irecommend)

    @property
    def rating_tripadvisor_str(self):
        return str(self.rating_tripadvisor)


@receiver(post_init, sender=Company)
def company_post_init(sender, instance, ** kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


class Membership(Model):
    """ Личная настройка для филиала """
    class Meta:
        db_table = "resources_membership"
        verbose_name = "участник"
        verbose_name_plural = "участники"

    """ Настройки """
    is_owner = BooleanField(default=False, verbose_name="владелец?")
    is_notify_0 = BooleanField(default=True, verbose_name="оповещать с 0 звезд?")
    is_notify_1 = BooleanField(default=True, verbose_name="оповещать с 1 звездой?")
    is_notify_2 = BooleanField(default=True, verbose_name="оповещать с 2 звездами?")
    is_notify_3 = BooleanField(default=True, verbose_name="оповещать с 3 звездами?")
    is_notify_4 = BooleanField(default=True, verbose_name="оповещать с 4 звездами?")
    is_notify_5 = BooleanField(default=True, verbose_name="оповещать с 5 звездами?")
    is_notify_portrate = BooleanField(default=True, verbose_name="оповещать Портрет?")
    is_notify_yandex = BooleanField(default=True, verbose_name="оповещать Яндекс?")
    is_notify_gis = BooleanField(default=True, verbose_name="оповещать 2Гис?")
    is_notify_google = BooleanField(default=True, verbose_name="оповещать Google?")
    is_notify_avito = BooleanField(default=True, verbose_name="оповещать Авито?")
    is_notify_zoon = BooleanField(default=True, verbose_name="оповещать Zoon?")
    is_notify_flamp = BooleanField(default=True, verbose_name="оповещать Flamp?")
    is_notify_yell = BooleanField(default=True, verbose_name="оповещать Yell?")
    is_notify_prodoctorov = BooleanField(default=True, verbose_name="оповещать Продокторов?")
    is_notify_yandex_services = BooleanField(default=True, verbose_name="оповещать Яндекс услуги?")
    is_notify_otzovik = BooleanField(default=True, verbose_name="оповещать Otzovik?")
    is_notify_irecommend = BooleanField(default=True, verbose_name="оповещать Irecommend?")
    is_notify_tripadvisor = BooleanField(default=True, verbose_name="оповещать Tripadvisor?")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE)
    user = ForeignKey("auth.User", on_delete=CASCADE)

    def __str__(self):
        return f"{self.company} → {self.user}"


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
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="филиал")
    visit_stamp = ForeignKey("resources.VisitStamp", on_delete=CASCADE, verbose_name="отпечаток перехода на форму запроса отзывов")

    def __str__(self):
        return f"{self.company} → {self.created_at}"

    @property
    def notification_template(self):
        return f"""Новое сообщение: {self.company.name}

{self.phone}
{self.text}
{localize(self.created_at)}"""


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, ** kwargs):
    if created:
        for user in instance.company.users.filter(membership__is_notify_portrate=True).exclude(profile__telegram_id=None).all():
            asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(user.profile.telegram_id, instance.notification_template))


class Payment(Model):
    """ Платеж """
    class Meta:
        db_table = "resources_payment"
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    """ Автогенерация """
    created_at = DateTimeField(auto_now_add=True, verbose_name="дата создания")
    api_secret = CharField(db_index=True, verbose_name="№ заказа")

    """ Данные """
    rate = CharField(choices=Rate.choices, default=Rate.START, verbose_name="тариф")
    period = CharField(choices=Period.choices, default=Period.ANNUALLY, verbose_name="период")
    amount = MoneyField(default=0, default_currency="RUB", decimal_places=2, max_digits=14, verbose_name="сумма")
    is_paid = BooleanField(default=False, verbose_name="оплачен?")
    paid_at = DateTimeField(blank=True, null=True, verbose_name="дата оплаты")
    card_id = CharField(blank=True, null=True, verbose_name="ID карты")

    """ Связи """
    user = ForeignKey("auth.User", on_delete=CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f"{self.user} → {self.created_at}"


@receiver(post_init, sender=Payment)
def payment_post_init(sender, instance, ** kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


class Profile(Model):
    """ Профиль """
    class Meta:
        db_table = "resources_profile"
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    """ Автогенерация """
    api_secret = CharField(db_index=True, verbose_name="API ключ")
    balance = MoneyField(default=60, default_currency="RUB", decimal_places=2,  max_digits=14, verbose_name="баланс")

    """ Настройки """
    default_timezone = CharField(choices=Timezone.choices, default=Timezone.UTC, verbose_name="временная зона по умолчанию")
    telegram_id = CharField(blank=True, null=True, verbose_name="telegram ID")
    rate = CharField(choices=Rate.choices, default=Rate.START, verbose_name="тариф")

    start_price_monthly_base = MoneyField(default=250, default_currency="RUB", decimal_places=2, max_digits=14, verbose_name="стоимость тарифа Старт, в месяц")
    regular_price_monthly_base = MoneyField(default=500, default_currency="RUB", decimal_places=2, max_digits=14, verbose_name="стоимость тарифа Стандарт, в месяц")
    business_price_monthly_base = MoneyField(default=1500, default_currency="RUB", decimal_places=2, max_digits=14, verbose_name="стоимость тарифа Бизнес, в месяц")

    start_max_count = IntegerField(default=1, verbose_name="максимальное количество филиалов тарифа Старт")
    regular_max_count = IntegerField(default=3, verbose_name="максимальное количество филиалов тарифа Стандарт")
    business_max_count = IntegerField(default=10, verbose_name="максимальное количество филиалов тарифа Бизнес")

    """ Связи """
    user = OneToOneField("auth.User", on_delete=CASCADE)

    def __str__(self):
        return str(self.user.username)

    """ Стоимость тарифов """
    @property
    def start_price_monthly(self):
        return float(self.start_price_monthly_base.amount)

    @property
    def start_price_monthly_sale(self):
        return float(self.start_price_monthly_base.amount)

    @property
    def start_price_monthly_display(self):
        return float(self.start_price_monthly_base.amount)

    @property
    def start_price_annually(self):
        return float(self.start_price_monthly * 12)

    @property
    def start_price_annually_sale(self):
        return float(self.start_price_annually * 0.7)

    @property
    def start_price_annually_display(self):
        return float(self.start_price_monthly * 0.7)

    @property
    def regular_price_monthly(self):
        return float(self.regular_price_monthly_base.amount)

    @property
    def regular_price_monthly_sale(self):
        return float(self.regular_price_monthly_base.amount)

    @property
    def regular_price_monthly_display(self):
        return float(self.regular_price_monthly_base.amount)

    @property
    def regular_price_annually(self):
        return float(self.regular_price_monthly * 12)

    @property
    def regular_price_annually_sale(self):
        return float(self.regular_price_annually * 0.7)

    @property
    def regular_price_annually_display(self):
        return float(self.regular_price_monthly * 0.7)

    @property
    def business_price_monthly(self):
        return float(self.business_price_monthly_base.amount)

    @property
    def business_price_monthly_sale(self):
        return float(self.business_price_monthly_base.amount)

    @property
    def business_price_monthly_display(self):
        return float(self.business_price_monthly_base.amount)

    @property
    def business_price_annually(self):
        return float(self.business_price_monthly * 12)

    @property
    def business_price_annually_sale(self):
        return float(self.business_price_annually * 0.7)

    @property
    def business_price_annually_display(self):
        return float(self.business_price_monthly * 0.7)

    @property
    def day_price(self):
        return round(float(self.__getattribute__(f"{self.rate.lower()}_price_annually") / 365), 2)

    @property
    def days_left(self):
        return math.floor(float(self.balance.amount) / self.day_price)

    @property
    def end_at(self):
        return date.today() + timedelta(days=self.days_left)

    @property
    def is_active(self):
        return self.days_left > 0

    @property
    def can_create_company(self):
        count = Membership.objects.filter(user=self.user).count()

        if self.rate == Rate.START:
            return count < self.start_max_count
        elif self.rate == Rate.REGULAR:
            return count < self.regular_max_count
        elif self.rate == Rate.BUSINESS:
            return count < self.business_max_count

    @property
    def can_parse_yandex(self):
        return self.rate in [Rate.START, Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_gis(self):
        return self.rate in [Rate.START, Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_google(self):
        return self.rate in [Rate.START, Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_avito(self):
        return self.rate in [Rate.START, Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_zoon(self):
        return self.rate in [Rate.START, Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_flamp(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_yell(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_prodoctorov(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_yandex_services(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_otzovik(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_irecommend(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]

    @property
    def can_parse_tripadvisor(self):
        return self.rate in [Rate.REGULAR, Rate.BUSINESS]


@receiver(post_init, sender=Profile)
def profile_post_init(sender, instance, ** kwargs):
    if not instance.api_secret:
        instance.api_secret = get_random_string(length=8)


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
    is_visible = BooleanField(default=True, verbose_name="отображается в виджете?")
    is_moderated = BooleanField(default=False, verbose_name="отмодерирован?")

    """ Контент """
    remote_id = CharField(db_index=True, verbose_name="ID (агрегация)")
    service = CharField(choices=Service.choices, default=Service.YANDEX, verbose_name="сервис")
    stars = IntegerField(default=0, verbose_name="оценка")
    name = CharField(verbose_name="пользователь")
    text = TextField(verbose_name="текст отзыва")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="филиал")

    def __str__(self):
        return f"{self.company} → {self.service} - {self.created_at}"

    @property
    def stars_float(self):
        return float(self.stars)

    @property
    def stars_str(self):
        return str(self.stars_float)

    @property
    def notification_template(self):
        return f"""Новый отзыв: {self.company.name}

{self.get_service_display()}: {self.stars * '⭐️'}
{self.text if self.text else 'Оценка без текста'}
{self.name}, {localize(self.created_at)}"""


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, ** kwargs):
    if created and not instance.company.__getattribute__(f"is_first_parsing_{instance.service.lower()}"):
        for user in instance.company.users.filter(
            ** {
                f"membership__is_notify_{instance.service.lower()}": True,
                f"membership__is_notify_{instance.stars}": True
            }
        ).exclude(profile__telegram_id=None).all():
            asyncio.run(Bot(settings.TELEGRAM_BOT_API_SECRET).send_message(user.profile.telegram_id, instance.notification_template))


class Story(Model):
    """ Платеж """
    class Meta:
        db_table = "resources_story"
        verbose_name = "история"
        verbose_name_plural = "истории"

    """ Автогенерация """
    created_at = DateTimeField(auto_now_add=True, verbose_name="дата создания")

    """ Настройки """
    is_active = BooleanField(default=False, verbose_name="активно?")
    is_visible_master = BooleanField(default=False, verbose_name="отображать в мастере?")
    is_visible_finance = BooleanField(default=False, verbose_name="отображать в тарифах?")
    is_visible_profile = BooleanField(default=False, verbose_name="отображать в профиле?")
    is_visible_home = BooleanField(default=False, verbose_name="отображать в списке филиалов?")
    is_visible_statistic = BooleanField(default=False, verbose_name="отображать в статистике?")
    is_visible_reviews = BooleanField(default=False, verbose_name="отображать в отзывах?")
    is_visible_messages = BooleanField(default=False, verbose_name="отображать в жалобах?")
    is_visible_widget = BooleanField(default=False, verbose_name="отображать в виджете?")
    is_visible_feedback = BooleanField(default=False, verbose_name="отображать в визитке?")
    is_visible_qr = BooleanField(default=False, verbose_name="отображать в списке qr?")
    is_visible_notifications = BooleanField(default=False, verbose_name="отображать в уведомлениях?")

    """ Данные """
    name = CharField(verbose_name="название")
    preview = ResizedImageField(crop=['middle', 'center'], size=[256, 256], upload_to="dashboard/%Y/%m/%d/", verbose_name="превью")
    video = FileField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="видео")
    image = ImageField(blank=True, null=True, upload_to="dashboard/%Y/%m/%d/", verbose_name="изображение")

    """ Связи """
    users = ManyToManyField("auth.User", blank=True, verbose_name="пользователи")

    @property
    def is_video(self):
        if self.video:
            return True
        else:
            return False

    @property
    def media(self):
        if self.video:
            return self.video
        elif self.image:
            return self.image
        else:
            return None

    def __str__(self):
        return str(self.name)


class VisitStamp(Model):
    """ Отпечаток перехода на форму запроса отзывов """
    class Meta:
        db_table = "resources_visit_stamp"
        verbose_name = "Отпечаток перехода на форму запроса отзывов"
        verbose_name_plural = "Отпечатки перехода на форму запроса отзывов"

    """ Первичный ключ """
    id = CharField(max_length=40, primary_key=True)

    """ Автогенерация """
    created_at = DateField(auto_now_add=True, verbose_name="дата создания")

    """ Контент """
    utm_source = CharField(blank=True, null=True, verbose_name="источник")

    """ Связи """
    company = ForeignKey("resources.Company", on_delete=CASCADE, verbose_name="филиал")

    def __str__(self):
        return f"{self.company} → {self.utm_source} - {self.created_at}"
