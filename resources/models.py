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
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Портрет'
    )

    portrate_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Портрет'
    )

    yandex_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Яндекс'
    )

    yandex_rate_stars = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='звезды Яндекс'
    )

    yandex_rate_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество оценок Яндекс'
    )

    yandex_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Яндекс'
    )

    yandex_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Яндекс'
    )

    yandex_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Яндекс'
    )

    yandex_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Яндекс'
    )

    gis_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг 2Гис'
    )

    gis_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов 2Гис'
    )

    gis_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов 2Гис'
    )

    gis_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга 2Гис'
    )

    gis_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов 2Гис'
    )

    google_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Google'
    )

    google_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Google'
    )

    google_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Google'
    )

    google_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Google'
    )

    google_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Google'
    )

    mapsme_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Mapsme'
    )

    mapsme_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Mapsme'
    )

    mapsme_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Mapsme'
    )

    mapsme_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Mapsme'
    )

    mapsme_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Mapsme'
    )

    dikidi_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Dikidi'
    )

    dikidi_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Dikidi'
    )

    dikidi_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Dikidi'
    )

    dikidi_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Dikidi'
    )

    dikidi_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Dikidi'
    )

    restoclub_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Рестоклуб'
    )

    restoclub_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Рестоклуб'
    )

    restoclub_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Рестоклуб'
    )

    restoclub_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Рестоклуб'
    )

    restoclub_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Рестоклуб'
    )

    tripadvisor_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Tripadvisor'
    )

    tripadvisor_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Tripadvisor'
    )

    tripadvisor_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Tripadvisor'
    )

    tripadvisor_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Tripadvisor'
    )

    tripadvisor_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Tripadvisor'
    )

    prodoctorov_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Продокторов'
    )

    prodoctorov_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Продокторов'
    )

    prodoctorov_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Продокторов'
    )

    prodoctorov_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Продокторов'
    )

    prodoctorov_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Продокторов'
    )

    flamp_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Flamp'
    )

    flamp_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Flamp'
    )

    flamp_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Flamp'
    )

    flamp_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Flamp'
    )

    flamp_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Flamp'
    )

    zoon_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Zoon'
    )

    zoon_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Zoon'
    )

    zoon_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Zoon'
    )

    zoon_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Zoon'
    )

    zoon_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Zoon'
    )

    otzovik_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Отзовик'
    )

    otzovik_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Отзовик'
    )

    otzovik_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Отзовик'
    )

    otzovik_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Отзовик'
    )

    otzovik_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Отзовик'
    )

    irecommend_rate = models.DecimalField(
        blank=True,
        decimal_places=1,
        default=0.0,
        max_digits=10,
        null=True,
        verbose_name='рейтинг Irecommend'
    )

    irecommend_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов Irecommend'
    )

    irecommend_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов Irecommend'
    )

    irecommend_rate_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки рейтинга Irecommend'
    )

    irecommend_reviews_last_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='дата последней загрузки отзывов Irecommend'
    )

    total_positive_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество позитивных отзывов всего'
    )

    total_negative_count = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='количество негативных отзывов всего'
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
        unique_together = ('company', 'remote_id',)

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
        verbose_name='дата создания'
    )

    from_bot = models.BooleanField(
        default=False,
        verbose_name='Отправлено ботом Портрет'
    )

    remote_id = models.CharField(
        blank=True,
        null=True,
        verbose_name='ID (агрегация)'
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
        blank=True,
        null=True,
        verbose_name='пользователь'
    )

    text = models.TextField(
        blank=True,
        null=True,
        verbose_name='текст отзыва'
    )

    answer = models.TextField(
        blank=True,
        null=True,
        verbose_name='текст ответа'
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

    review = models.OneToOneField(
        Review,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )

    def __str__(self):
        return str(self.text)


# Сигналы модели NegativeMessage
@receiver(post_save, sender=NegativeMessage)
def negativemessage_post_save_signal(sender, instance, created, **kwargs):
    if created:
        instance.company.portrate_negative_count = instance.company.negativemessage_set.count()
        instance.company.save()


# Сигналы модели Review
@receiver(post_save, sender=Review)
def review_post_save_signal(sender, instance, created, **kwargs):
    if created:

        instance.company.yandex_negative_count = instance.company.review_set.filter(
            service=Review.Service.YANDEX,
            rate__lt=4
        ).count()

        instance.company.yandex_positive_count = instance.company.review_set.filter(
            service=Review.Service.YANDEX,
            rate__gt=3
        ).count()

        instance.company.total_negative_count = instance.company.review_set.filter(rate__lt=4).count()
        instance.company.total_positive_count = instance.company.review_set.filter(rate__gt=3).count()
        instance.company.save()


# Сигналы модели Notification
@receiver(post_save, sender=Notification)
def notification_post_save_signal(sender, instance, created, **kwargs):

    # Негативное сообщение из формы запроса отзыва
    if created and instance.initiator == Notification.Initiator.PORTRATE_NEGATIVE_MESSAGE:
        # Шаблон
        text = f'''📍 Негативное сообщение в Портрете.

🏪 Компания:
{instance.negative_message.company}

📱 Телефон:
{instance.negative_message.phone}

📜 Комментарий:
{instance.negative_message.text}'''

        for user in instance.company.users.exclude(profile__telegram_id=None).all():
            send_telegram_text_task.delay(user.profile.telegram_id, text)

    # Негативное сообщение из формы запроса отзыва
    elif created and instance.initiator == Notification.Initiator.YANDEX_NEGATIVE_REVIEW:
        # Шаблон
        text = f'''📍 Негативный отзыв в Яндексе.

🏪 Компания:
{instance.review.company}

📜 Текст:
{instance.review.text}'''

        for user in instance.company.users.exclude(profile__telegram_id=None).all():
            send_telegram_text_task.delay(user.profile.telegram_id, text)
