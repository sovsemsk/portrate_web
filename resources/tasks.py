from datetime import datetime, timezone, timedelta
from hashlib import md5

from celery import shared_task
from django.core.cache import cache

from parsers.parser_gis import ParserGis
from parsers.parser_google import ParserGoogle
from parsers.parser_yandex import ParserYandex
from resources.models import Company, Review, RatingStamp, Service


def locked_task(func):
    def wrapper(*args, **kwargs):
        lock_id = f"_{args[0].name}_lock_{md5(str(args).encode('utf-8')).hexdigest()}_{md5(str(kwargs).encode('utf-8')).hexdigest()}_"

        if cache.get(lock_id):
            return "Already run"

        cache.set(lock_id, lock_id)
        func(*args, **kwargs)
        cache.delete(lock_id)

    return wrapper


@shared_task(bind=True, name="update_yandex_task")
@locked_task
def update_yandex_task(self, *args, **kwargs):
    company = Company.objects.get(pk=kwargs.get("company_id"))
    parser_yandex = ParserYandex(company.parser_link_yandex)

    if parser_yandex.check_page():
        company.rating_yandex = parser_yandex.parse_rating()

        for r in parser_yandex.parse_reviews():
            try:
                Review.objects.create(company_id=company.id, service=Service.YANDEX, **r)
            except:
                ...

        company.rating_yandex_last_parse_at = datetime.now(timezone.utc)
        company.reviews_yandex_last_parse_at = datetime.now(timezone.utc)

    company.save(update_fields=["rating_yandex", "rating_yandex_last_parse_at", "reviews_yandex_last_parse_at"])
    parser_yandex.close_page()
    return f"Done for {company}"


@shared_task(bind=True, name="update_gis_task")
@locked_task
def update_gis_task(self, *args, **kwargs):
    company = Company.objects.get(pk=kwargs.get("company_id"))
    parser_gis = ParserGis(company.parser_link_gis)

    if parser_gis.check_page():
        company.rating_gis = parser_gis.parse_rating()

        for r in parser_gis.parse_reviews():
            try:
                Review.objects.create(company_id=company.id, service=Service.GIS, **r)
            except:
                ...

        company.rating_gis_last_parse_at = datetime.now(timezone.utc)
        company.reviews_gis_last_parse_at = datetime.now(timezone.utc)

    company.save(update_fields=["rating_gis", "rating_gis_last_parse_at", "reviews_gis_last_parse_at"])
    parser_gis.close_page()
    return f"Done for {company}"


@shared_task(bind=True, name="update_google_task")
@locked_task
def update_google_task(self, *args, **kwargs):
    company = Company.objects.get(pk=kwargs.get("company_id"))
    parser_google = ParserGoogle(company.parser_link_google)

    if parser_google.check_page():
        company.rating_google = parser_google.parse_rating()

        for r in parser_google.parse_reviews():
            try:
                Review.objects.create(company_id=company.id, service=Service.GOOGLE, **r)
            except:
                ...

        company.rating_google_last_parse_at = datetime.now(timezone.utc)
        company.reviews_google_last_parse_at = datetime.now(timezone.utc)

    company.save(update_fields=["rating_google", "rating_google_last_parse_at", "reviews_google_last_parse_at"])
    parser_google.close_page()
    return f"Done for {company}"


@shared_task(bind=True, name="update_counters_task")
@locked_task
def update_counters_task(self, *args, **kwargs):
    company = Company.objects.get(pk=kwargs.get("company_id"))

    reviews_yandex = company.review_set.filter(service=Service.YANDEX)
    reviews_gis = company.review_set.filter(service=Service.GIS)
    reviews_google = company.review_set.filter(service=Service.GOOGLE)

    date_week_ago = datetime.today() - timedelta(days=7)
    date_month_ago = datetime.today() - timedelta(days=30)
    date_quarter_ago = datetime.today() - timedelta(days=90)
    date_year_ago = datetime.today() - timedelta(days=365)

    company.reviews_yandex_negative_count = reviews_yandex.filter(stars__lte=3).count()
    company.reviews_yandex_negative_week_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_negative_month_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_negative_quarter_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_negative_year_count = reviews_yandex.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_yandex_positive_count = reviews_yandex.filter(stars__gt=3).count()
    company.reviews_yandex_positive_week_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_positive_month_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_positive_quarter_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_positive_year_count = reviews_yandex.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_yandex_total_count = reviews_yandex.count()
    company.reviews_yandex_total_week_count = reviews_yandex.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_total_month_count = reviews_yandex.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_total_quarter_count = reviews_yandex.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_yandex_total_year_count = reviews_yandex.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_gis_negative_count = reviews_gis.filter(stars__lte=3).count()
    company.reviews_gis_negative_week_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_negative_month_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_negative_quarter_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_negative_year_count = reviews_gis.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_gis_positive_count = reviews_gis.filter(stars__gt=3).count()
    company.reviews_gis_positive_week_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_positive_month_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_positive_quarter_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_positive_year_count = reviews_gis.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_gis_total_count = reviews_gis.count()
    company.reviews_gis_total_week_count = reviews_gis.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_total_month_count = reviews_gis.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_total_quarter_count = reviews_gis.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_gis_total_year_count = reviews_gis.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_google_negative_count = reviews_google.filter(stars__lte=3).count()
    company.reviews_google_negative_week_count = reviews_google.filter(stars__lte=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_negative_month_count = reviews_google.filter(stars__lte=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_negative_quarter_count = reviews_google.filter(stars__lte=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_negative_year_count = reviews_google.filter(stars__lte=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_google_positive_count = reviews_google.filter(stars__gt=3).count()
    company.reviews_google_positive_week_count = reviews_google.filter(stars__gt=3, created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_positive_month_count = reviews_google.filter(stars__gt=3, created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_positive_quarter_count = reviews_google.filter(stars__gt=3, created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_positive_year_count = reviews_google.filter(stars__gt=3, created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_google_total_count = reviews_google.count()
    company.reviews_google_total_week_count = reviews_google.filter(created_at__gt=date_week_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_total_month_count = reviews_google.filter(created_at__gt=date_month_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_total_quarter_count = reviews_google.filter(created_at__gt=date_quarter_ago, created_at__lte=datetime.today()).count()
    company.reviews_google_total_year_count = reviews_google.filter(created_at__gt=date_year_ago, created_at__lte=datetime.today()).count()

    company.reviews_total_count = Review.objects.filter(company_id=company.id).count()
    company.rating = max([company.rating_yandex, company.rating_gis, company.rating_google])
    company.is_first_parsing = False

    company.save(update_fields=[
        "reviews_yandex_negative_count",
        "reviews_yandex_negative_week_count",
        "reviews_yandex_negative_month_count",
        "reviews_yandex_negative_quarter_count",
        "reviews_yandex_negative_year_count",
        "reviews_yandex_positive_count",
        "reviews_yandex_positive_week_count",
        "reviews_yandex_positive_month_count",
        "reviews_yandex_positive_quarter_count",
        "reviews_yandex_positive_year_count",
        "reviews_yandex_total_count",
        "reviews_yandex_total_week_count",
        "reviews_yandex_total_month_count",
        "reviews_yandex_total_quarter_count",
        "reviews_yandex_total_year_count",
        "reviews_gis_negative_count",
        "reviews_gis_negative_week_count",
        "reviews_gis_negative_month_count",
        "reviews_gis_negative_quarter_count",
        "reviews_gis_negative_year_count",
        "reviews_gis_positive_count",
        "reviews_gis_positive_week_count",
        "reviews_gis_positive_month_count",
        "reviews_gis_positive_quarter_count",
        "reviews_gis_positive_year_count",
        "reviews_gis_total_count",
        "reviews_gis_total_week_count",
        "reviews_gis_total_month_count",
        "reviews_gis_total_quarter_count",
        "reviews_gis_total_year_count",
        "reviews_google_negative_count",
        "reviews_google_negative_week_count",
        "reviews_google_negative_month_count",
        "reviews_google_negative_quarter_count",
        "reviews_google_negative_year_count",
        "reviews_google_positive_count",
        "reviews_google_positive_week_count",
        "reviews_google_positive_month_count",
        "reviews_google_positive_quarter_count",
        "reviews_google_positive_year_count",
        "reviews_google_total_count",
        "reviews_google_total_week_count",
        "reviews_google_total_month_count",
        "reviews_google_total_quarter_count",
        "reviews_google_total_year_count",
        "reviews_total_count",
        "rating",
        "is_first_parsing"
    ])

    try:
        RatingStamp.objects.create(company_id=company.id, rating_yandex=company.rating_yandex, rating_gis=company.rating_gis, rating_google=company.rating_google)
    except:
        ...

    return f"Done for {company}"

