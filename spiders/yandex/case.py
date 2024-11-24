import hashlib
import re
from datetime import datetime, timezone

import dateparser
from django.db import IntegrityError

from resources.models import Company, Review, Service
from spiders.yandex.reviews_page import ReviewsPage
from spiders.utils import Driver


def perform(company_id):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_yandex = True
    company.save(update_fields=["is_parser_run_yandex"])

    # Парсинг
    with Driver() as web_driver:
        web_driver.get(company.parser_link_yandex)
        reviews_page = ReviewsPage(web_driver)
        reviews_page.order_all()
        reviews_page.show_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at, languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_yandex),
                    remote_id=hashlib.md5(f"{review.name}{review.created_at}".encode()).hexdigest(),
                    service=Service.YANDEX,
                    stars=review.stars,
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except IntegrityError:
                pass

        company.rating_yandex = float(".".join(re.findall(r"\d+", reviews_page.rating))) if reviews_page.rating else None
        company.reviews_count_remote_yandex = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_yandex", "reviews_count_remote_yandex"])

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_yandex = False
    company.is_first_parsing_yandex = False
    company.parser_last_parse_at_yandex = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_yandex", "parser_last_parse_at_yandex", "is_parser_run_yandex"])