from hashlib import md5

import celery
from celery import chain, shared_task
from django.contrib.auth.models import User
from django.core.cache import cache
from djmoney.money import Money

from parsers.yandex import perform as yandex_perform
from parsers.gis import perform as gis_perform
from parsers.google import perform as google_perform
from parsers.avito import perform as avito_perform
from resources.models import Company


@shared_task(name="parse_yandex_task")
def parse_yandex_task(previous_result=None, company_id=None):
    lock_id = f"_parse_yandex_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    yandex_perform(company_id, celery.current_task)

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


@shared_task(name="parse_gis_task")
def parse_gis_task(previous_result=None, company_id=None):
    lock_id = f"_parse_gis_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    gis_perform(company_id, celery.current_task)

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


@shared_task(name="parse_google_task")
def parse_google_task(previous_result=None, company_id=None):
    lock_id = f"_parse_google_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    google_perform(company_id, celery.current_task)

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


@shared_task(name="parse_avito_task")
def parse_avito_task(previous_result=None, company_id=None):
    lock_id = f"_parse_avito_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    avito_perform(company_id, celery.current_task)

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


@shared_task(name="parse_zoon_task")
def parse_zoon_task(previous_result=None, company_id=None):
    lock_id = f"_parse_zoon_task_lock_{md5(str(company_id).encode('utf-8')).hexdigest()}_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    # cache.set(lock_id, lock_id)

    """ Задача """

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


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
    return True


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
    return True


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
    return True


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
    return True


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
    return True


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
    return True


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
    return True


@shared_task(name="parse_all")
def parse_all_task():
    lock_id = f"_parse_all_task_lock_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    companies = Company.objects.all()

    for company in companies:
        parsers_chain = []

        if company.is_active:
            if company.can_parse_yandex and company.parser_link_yandex:
                parsers_chain.append(parse_yandex_task.s(company_id=company.id))

            if company.can_parse_gis and company.parser_link_gis:
                parsers_chain.append(parse_gis_task.s(company_id=company.id))

            if company.can_parse_google and company.parser_link_google:
                parsers_chain.append(parse_google_task.s(company_id=company.id))

            if company.can_parse_avito and company.parser_link_avito:
                parsers_chain.append(parse_avito_task.s(company_id=company.id))

            chain(*parsers_chain).apply_async()

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True


@shared_task(name="withdraw_all")
def withdraw_all_task():
    lock_id = f"_withdraw_all_task_lock_"

    """ Отмена выполнения если уже есть блокировка """
    if cache.get(lock_id):
        return

    """ Блокировка для выполнения """
    cache.set(lock_id, lock_id)

    """ Задача """
    users = User.objects.select_related("profile").all()

    for user in users:
        if user.profile.is_active:
            user.profile.balance = Money(float(user.profile.balance.amount) - user.profile.day_price, "RUB")
            user.save()

    """ Разблокировка для выполнения """
    cache.delete(lock_id)
    return True