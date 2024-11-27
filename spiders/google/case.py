import re
from datetime import datetime, timezone

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException

from resources.models import Company, Review, Service
from spiders.google.reviews_page import ReviewsPage
from spiders.utils import Driver, extract_int, extract_float


def perform(company_id):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_google = True
    company.save(update_fields=["is_parser_run_google"])

    # Парсинг
    with Driver() as web_driver:
        web_driver.get(company.parser_link_google)
        reviews_page = ReviewsPage(web_driver)
        reviews_page.order_all()
        reviews_page.show_all()
        # reviews_page.expand_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at, languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_google),
                    remote_id=review.remote_id,
                    service=Service.GOOGLE,
                    stars=review.stars,
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except (AttributeError, IntegrityError, NoSuchElementException):
                pass

        company.rating_google = extract_float(reviews_page.rating)
        company.reviews_count_remote_google = extract_int(reviews_page.count)
        company.save(update_fields=["rating_google", "reviews_count_remote_google"])

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_google = False
    company.is_first_parsing_google = False
    company.parser_last_parse_at_google = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_google", "parser_last_parse_at_google", "is_parser_run_google"])
