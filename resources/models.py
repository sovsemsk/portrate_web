from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from resources.tasks import send_telegram_text_task


# Компания
class Company(models.Model):
    class Meta:
        db_table = 'resources_company'
        verbose_name = 'компания'
        verbose_name_plural = 'компании'

    # Настройки
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активно?'
    )

    yandex_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Яндекс'
    )

    is_yandex_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Яндекс?'
    )

    is_yandex_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Яндекс?'
    )

    gis_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Gis'
    )

    is_gis_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в 2Гис?'
    )

    is_gis_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с 2Гис?'
    )

    google_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Google'
    )

    is_google_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Google?'
    )

    is_google_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Google?'
    )

    mapsme_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Mapsme'
    )

    is_mapsme_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Mapsme?'
    )

    is_mapsme_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Mapsme?'
    )

    dikidi_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Dikidi'
    )

    is_dikidi_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Dikidi?'
    )

    is_dikidi_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Dikidi?'
    )

    restoclub_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Рестоклуб'
    )

    is_restoclub_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Рестоклуб?'
    )

    is_restoclub_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Рестоклуб?'
    )

    tripadvisor_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Tripadvisor'
    )

    is_tripadvisor_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Tripadvisor?'
    )

    is_tripadvisor_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Tripadvisor?'
    )

    prodoctorov_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Продокторов'
    )

    is_prodoctorov_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Продокторов?'
    )

    is_prodoctorov_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Продокторов?'
    )

    flamp_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Flamp'
    )

    is_flamp_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Flamp?'
    )

    is_flamp_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Flamp?'
    )

    zoon_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Zoon'
    )

    is_zoon_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Zoon?'
    )

    is_zoon_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Zoon?'
    )

    otzovik_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Отзовик'
    )

    is_otzovik_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Отзовик?'
    )

    is_otzovik_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Отзовик?'
    )

    irecommend_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID Irecommend'
    )

    is_irecommend_reviews_upload = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы в Irecommend?'
    )

    is_irecommend_reviews_download = models.BooleanField(
        default=False,
        verbose_name='Загружать отзывы с Irecommend?'
    )

    # Контент
    name = models.CharField(
        verbose_name='название'
    )

    address = models.CharField(
        verbose_name='адрес'
    )

    logo = models.ImageField(
        blank=True,
        null=True,
        upload_to='company_logo/%Y/%m/%d/',
        verbose_name='логотип'
    )

    request_form_home_head = models.TextField(
        default='Вам понравилось обслуживание?',
        verbose_name='Заголовок формы запроса отзыва (главная)'
    )

    request_form_positive_head = models.TextField(
        default='Наградите нас отзывом',
        verbose_name='Заголовок формы запроса отзыва (позитив)'
    )

    request_form_negative_head = models.TextField(
        default='Написать директору',
        verbose_name='Заголовок формы запроса отзыва (негатив)'
    )

    request_form_negative_text = models.TextField(
        default='Расскажите что вам не понравилось и что мы можем сделать лучше. Директор накажет виновных, свяжется с вами и предложит решение проблемы.',
        verbose_name='Текст формы запроса отзыва (негатив)'
    )

    request_form_tags = models.JSONField(
        default=[
            'Нагрубили',
            'Сделали не то',
            'Цена',
            'Плохое качество',
            'Долго'
        ],
        verbose_name='Теги формы запроса отзыва'
    )

    yandex_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Яндекс'
    )

    gis_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка 2Гис'
    )

    google_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Google'
    )

    mapsme_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Mapsme'
    )

    dikidi_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Dikidi'
    )

    restoclub_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Рестоклуб'
    )

    tripadvisor_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Tripadvisor'
    )

    prodoctorov_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Продокторов'
    )

    zoon_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Zoon'
    )

    otzovik_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Отзовик'
    )

    irecommend_link = models.CharField(
        blank=True,
        null=True,
        verbose_name='ссылка Irecommend'
    )

    # Агрегация
    portrate_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    portrate_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    yandex_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    yandex_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    yandex_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    gis_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    gis_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    gis_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    google_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    google_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    google_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    mapsme_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    mapsme_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    mapsme_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    dikidi_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    dikidi_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    dikidi_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    restoclub_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    restoclub_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    restoclub_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    tripadvisor_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    tripadvisor_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    tripadvisor_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    prodoctorov_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    prodoctorov_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    prodoctorov_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    flamp_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    flamp_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    flamp_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    zoon_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    zoon_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    zoon_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    otzovik_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    otzovik_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    otzovik_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    irecommend_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=None,
        max_digits=1,
        null=True
    )

    irecommend_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    irecommend_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    total_positive_count = models.IntegerField(
        blank=True,
        null=True
    )

    total_negative_count = models.IntegerField(
        blank=True,
        null=True
    )

    # Связи
    users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='пользователи'
    )

    def __str__(self):
        return self.name


# Негативное сообщение с Портрета
class NegativeMessage(models.Model):
    class Meta:
        db_table = 'resources_negative_message'
        verbose_name = 'негативное сообщение'
        verbose_name_plural = 'негативные сообщения'

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    phone = models.CharField(
        verbose_name='контактный телефон'
    )

    text = models.TextField(
        blank=True,
        null=True,
        verbose_name='текст сообщения'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='компания'
    )

    def __str__(self):
        return self.phone


# Отзыв
class Review(models.Model):
    class Meta:
        db_table = 'resources_review'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    class Service(models.TextChoices):
        YANDEX = 'YANDEX', 'Яндекс'
        GIS = 'GIS', '2Гис'
        GOOGLE = 'GOOGLE', 'Google'

    service = models.CharField(
        choices=Service.choices,
        default=Service.YANDEX,
        verbose_name='сервис'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    from_bot = models.BooleanField(
        default=False,
        verbose_name='Отправлено ботом Портрет'
    )

    remote_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID сервиса'
    )

    conversation_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID диалога'
    )

    rate = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='рейтинг'
    )

    avatar_url = models.CharField(
        blank=True,
        null=True,
        verbose_name='url аватара'
    )

    name = models.CharField(
        verbose_name='пользователь'
    )

    text = models.TextField(
        verbose_name='текст отзыва'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='сеть'
    )

    def __str__(self):
        return f'{self.name}'


# Оповещение
class Notification(models.Model):
    class Meta:
        db_table = 'resources_notification'
        verbose_name = 'оповещение'
        verbose_name_plural = 'оповещения'

    class Initiator(models.TextChoices):
        PORTRATE_NEGATIVE_MESSAGE = "PORTRATE_NEGATIVE_MESSAGE", "Негативное сообщение Портрет"

        YANDEX_NEGATIVE_REVIEW = "YANDEX_NEGATIVE_REVIEW", "Негативный отзыв Яндекс"
        GIS_NEGATIVE_REVIEW = "GIS_NEGATIVE_REVIEW", "Негативный отзыв 2Гис"
        GOOGLE_NEGATIVE_REVIEW = "GOOGLE_NEGATIVE_REVIEW", "Негативный отзыв Google"

        YANDEX_POSITIVE_REVIEW = "YANDEX_POSITIVE_REVIEW", "Позитивный отзыв Яндекс"
        GIS_REVIEW = "GIS_POSITIVE_REVIEW", "Позитивный отзыв 2Гис"
        GOOGLE_POSITIVE_REVIEW = "GOOGLE_POSITIVE_REVIEW", "Позитивный отзыв Google"

        YANDEX_PARSE_SUCCESS = "YANDEX_PARSE_SUCCESS", "Отзывы загружены Яндекс"
        GIS_PARSE_SUCCESS = "GIS_PARSE_SUCCESS", "Отзывы загружены 2Гис"
        GOOGLE_PARSE_SUCCESS = "GOOGLE_PARSE_SUCCESS", "Отзывы загружены Google"

        YANDEX_PARSE_ERROR = "YANDEX_PARSE_ERROR", "Ошибка загрузки Яндекс"
        GIS_PARSE_ERROR = "GIS_PARSE_ERROR", "Ошибка загрузки 2Гис"
        GOOGLE_PARSE_ERROR = "GOOGLE_PARSE_ERROR", "Ошибка загрузки Google"

    initiator = models.CharField(
        choices=Initiator.choices,
        default=Initiator.PORTRATE_NEGATIVE_MESSAGE,
        verbose_name='инициатор'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    text = models.TextField(
        verbose_name='текст оповещения'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='сеть'
    )

    negative_message = models.OneToOneField(
        NegativeMessage,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='негативное сообщение'
    )

    def __str__(self):
        return str(self.text)


# Сигналы модели Notification
@ receiver(post_save, sender=Notification)
def telegram_notify_signal(sender, instance, created, **kwargs):
    if created and instance.initiator == 'PORTRATE_NEGATIVE_MESSAGE':
        # Шаблон
        text = f'''📍 Негативное сообщение в Портрете.

🏪 Компания:
{instance.negative_message.company}

📱 Телефон:
{instance.negative_message.phone}

📜 Комментарий:
{instance.negative_message.text}'''

    # Отправка всем пользователям компании
    for user in instance.company.users.exclude(profile__telegram_id=None).all():
        send_telegram_text_task.delay(user.profile.telegram_id, text)
