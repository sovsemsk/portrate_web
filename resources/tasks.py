from datetime import datetime, timezone
from hashlib import md5

from celery import shared_task
from django.core.cache import cache
from django.db import IntegrityError

from parsers.parser_avito import ParserAvito
from parsers.parser_gis import ParserGis
from parsers.parser_google import ParserGoogle
from parsers.parser_zoon import ParserZoon
from parsers.parser_yandex import ParserYandex
from resources.models import Company, Review, Service


@shared_task(name="parse_yandex_task")
def parse_yandex_task(previous_result=None, company_id=None):
    lock_id = f"_parse_yandex_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    company = Company.objects.get(pk=company_id)
    company.is_parser_run_yandex = True
    company.save(update_fields=["is_parser_run_yandex"])

    parser = ParserYandex(company.parser_link_yandex)

    if parser.parse_rating():
        rating = parser.parse_rating()
        reviews = parser.parse_reviews()
    else:
        rating = 0.0
        reviews = []

    parser.close_page()

    company.is_first_parsing_yandex = False
    company.parser_last_parse_at_yandex = datetime.now(timezone.utc)
    company.is_parser_run_yandex = False
    company.rating_yandex = rating
    company.save(update_fields=["is_first_parsing_yandex", "parser_last_parse_at_yandex", "is_parser_run_yandex", "rating_yandex"])

    for review in reviews:
        try:
            Review.objects.create(
                company_id=company.id,
                is_visible=(company.__getattribute__(f"is_visible_{review['stars']}") and company.is_visible_yandex),
                service=Service.YANDEX,
                **review
            )
        except IntegrityError:
            ...

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return rating


@shared_task(name="parse_gis_task")
def parse_gis_task(previous_result=None, company_id=None):
    lock_id = f"_parse_gis_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    company = Company.objects.get(pk=company_id)
    company.is_parser_run_gis = True
    company.save(update_fields=["is_parser_run_gis"])

    parser = ParserGis(company.parser_link_gis)

    if parser.parse_rating():
        rating = parser.parse_rating()
        reviews = parser.parse_reviews()
    else:
        rating = 0.0
        reviews = []

    parser.close_page()

    company.is_first_parsing_gis = False
    company.parser_last_parse_at_gis = datetime.now(timezone.utc)
    company.is_parser_run_gis = False
    company.rating_gis = rating
    company.save(update_fields=["is_first_parsing_gis", "parser_last_parse_at_gis", "is_parser_run_gis", "rating_gis"])

    for review in reviews:
        try:
            Review.objects.create(
                company_id=company.id,
                is_visible=(company.__getattribute__(f"is_visible_{review['stars']}") and company.is_visible_gis),
                service=Service.GIS,
                **review
            )
        except IntegrityError:
            ...

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return rating


@shared_task(name="parse_google_task")
def parse_google_task(previous_result=None, company_id=None):
    lock_id = f"_parse_google_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    company = Company.objects.get(pk=company_id)
    company.is_parser_run_google = True
    company.save(update_fields=["is_parser_run_google"])

    parser = ParserGoogle(company.parser_link_google)

    if parser.parse_rating():
        rating = parser.parse_rating()
        reviews = parser.parse_reviews()
    else:
        rating = 0.0
        reviews = []

    parser.close_page()

    company.is_first_parsing_google = False
    company.parser_last_parse_at_google = datetime.now(timezone.utc)
    company.is_parser_run_google = False
    company.rating_google = rating
    company.save(update_fields=["is_first_parsing_google", "parser_last_parse_at_google", "is_parser_run_google", "rating_google"])

    for review in reviews:
        try:
            Review.objects.create(
                company_id=company.id,
                is_visible=(company.__getattribute__(f"is_visible_{review['stars']}") and company.is_visible_google),
                service=Service.GOOGLE,
                **review
            )
        except IntegrityError:
            ...

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return rating


@shared_task(name="parse_avito_task")
def parse_avito_task(previous_result=None, company_id=None):
    lock_id = f"_parse_avito_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    company = Company.objects.get(pk=company_id)
    company.is_parser_run_avito = True
    company.save(update_fields=["is_parser_run_avito"])

    parser = ParserAvito(company.parser_link_avito)

    if parser.parse_rating():
        rating = parser.parse_rating()
        reviews = parser.parse_reviews()
    else:
        rating = 0.0
        reviews = []

    parser.close_page()

    company.is_first_parsing_avito = False
    company.parser_last_parse_at_avito = datetime.now(timezone.utc)
    company.is_parser_run_avito = False
    company.rating_avito = rating
    company.save(update_fields=["is_first_parsing_avito", "parser_last_parse_at_avito", "is_parser_run_avito", "rating_avito"])

    for review in reviews:
        try:
            Review.objects.create(
                company_id=company.id,
                is_visible=(company.__getattribute__(f"is_visible_{review['stars']}") and company.is_visible_avito),
                service=Service.AVITO,
                **review
            )
        except IntegrityError:
            ...

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return rating


@shared_task(name="parse_zoon_task")
def parse_zoon_task(previous_result=None, company_id=None):
    lock_id = f"_parse_zoon_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    company = Company.objects.get(pk=company_id)
    company.is_parser_run_zoon = True
    company.save(update_fields=["is_parser_run_zoon"])

    parser = ParserZoon(company.parser_link_zoon)

    if parser.parse_rating():
        rating = parser.parse_rating()
        reviews = parser.parse_reviews()
    else:
        rating = 0.0
        reviews = []

    parser.close_page()

    company.is_first_parsing_zoon = False
    company.parser_last_parse_at_zoon = datetime.now(timezone.utc)
    company.is_parser_run_zoon = False
    company.rating_zoon = rating
    company.save(update_fields=["is_first_parsing_zoon", "parser_last_parse_at_zoon", "is_parser_run_zoon", "rating_zoon"])

    for review in reviews:
        try:
            if review["name"] != "Официальный комментарий заведения":
                Review.objects.create(
                    company_id=company.id,
                    is_visible=(company.__getattribute__(f"is_visible_{review['stars']}") and company.is_visible_zoon),
                    service=Service.ZOON,
                    **review
                )
        except IntegrityError:
            ...

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return rating


@shared_task(name="parse_flamp_task")
def parse_flamp_task(previous_result=None, company_id=None):
    lock_id = f"_parse_flamp_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_yell_task")
def parse_yell_task(previous_result=None, company_id=None):
    lock_id = f"_parse_yell_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_prodoctorov_task")
def parse_prodoctorov_task(previous_result=None, company_id=None):
    lock_id = f"_parse_prodoctorov_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_yandex_services_task")
def parse_yandex_services_task(previous_result=None, company_id=None):
    lock_id = f"_parse_yandex_services_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_otzovik_task")
def parse_otzovik_task(previous_result=None, company_id=None):
    lock_id = f"_parse_otzovik_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_irecommend_task")
def parse_irecommend_task(previous_result=None, company_id=None):
    lock_id = f"_parse_irecommend_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0


@shared_task(name="parse_tripadvisor_task")
def parse_tripadvisor_task(previous_result=None, company_id=None):
    lock_id = f"_parse_tripadvisor_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return 0.0
