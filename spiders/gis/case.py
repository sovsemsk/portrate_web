import hashlib
import re
from datetime import datetime, timezone

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException

from resources.models import Company, Review, Service
from spiders.gis.reviews_page import ReviewsPage
from spiders.utils import Driver


def perform(company_id):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_gis = True
    company.save(update_fields=["is_parser_run_gis"])

    # Парсинг
    with Driver() as web_driver:
        web_driver.get(company.parser_link_gis)
        reviews_page = ReviewsPage(web_driver)
        reviews_page.close_promo()
        reviews_page.show_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at.replace(", отредактирован", ""), languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_gis),
                    remote_id=hashlib.md5(f"{review.name}{review.created_at}".encode()).hexdigest(),
                    service=Service.GIS,
                    stars=review.stars,
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except (AttributeError, IntegrityError, NoSuchElementException):
                pass

        company.rating_gis = float(".".join(re.findall(r"\d+", reviews_page.rating))) if reviews_page.rating else None
        company.reviews_count_remote_gis = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_gis", "reviews_count_remote_gis"])

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_gis = False
    company.is_first_parsing_gis = False
    company.parser_last_parse_at_gis = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_gis", "parser_last_parse_at_gis", "is_parser_run_gis"])