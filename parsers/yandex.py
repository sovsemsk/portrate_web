from datetime import datetime, timezone
import hashlib
import logging
import re
import time

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from parsers.driver import driver
from resources.models import Company, Review, Service

logger = logging.getLogger(__name__)


class StartPage():
    _tab_locator = (By.XPATH, ".//div[@class='tabs-select-view__title _name_reviews']")
    _url = None

    def __init__(self, driver):
        self.driver = driver
        time.sleep(10)

    def open_reviews(self):
        try:
            self.driver.find_element(*self._tab_locator).click()
            time.sleep(5)
            self._url = self.driver.current_url
        except (AttributeError, NoSuchElementException):
            pass

        return self

    @property
    def url(self):
        return self._url


class ReviewsPage():
    _rating_locator = (By.XPATH, ".//div[@class='business-summary-rating-badge-view__rating']")
    _count_locator = (By.XPATH, ".//h2[@class='card-section-header__title _wide']")
    _review_locator = (By.XPATH, ".//div[@class='business-reviews-card-view__review']")
    _dropdown_locator = (By.XPATH, ".//div[@class='rating-ranking-view']")
    _order_locator = (By.XPATH, ".//div[@aria-label='По новизне']")

    def __init__(self, driver):
        self.driver = driver
        time.sleep(10)

    def _scroll_more_(self, node):
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)
        new_nods = self.driver.find_elements(*self._review_locator)
        new_node = new_nods[-1]

        if node == new_node or len(new_nods) >= 500:
            return

        self._scroll_more_(new_node)

    def show_all(self):
        nodes = self.driver.find_elements(*self._review_locator)

        if len(nodes) > 0:
            self._scroll_more_(nodes[-1])

        return self

    def order_all(self):
        self.driver.find_element(*self._dropdown_locator).click()
        time.sleep(5)
        self.driver.find_element(*self._order_locator).click()
        time.sleep(5)
        return self

    @property
    def rating(self):
        try:
            return self.driver.find_element(*self._rating_locator).get_attribute("textContent")
        except (AttributeError, NoSuchElementException):
            return None

    @property
    def count(self):
        try:
            return self.driver.find_element(*self._count_locator).get_attribute("textContent")
        except (AttributeError, NoSuchElementException):
            return None

    @property
    def reviews(self):
        result = []

        for index, el in enumerate(self.driver.find_elements(*self._review_locator)):
            result.append(self.Review(el))

            if index == 99:
                break

        return result


    class Review():
        _created_at_locator = (By.XPATH, ".//meta[@itemprop='datePublished']")
        _stars_locator = (By.XPATH, ".//span[@class='inline-image _loaded icon business-rating-badge-view__star _full']")
        _name_locator = (By.XPATH, ".//span[@itemprop='name']")
        _text_locator = (By.XPATH, ".//span[@class='business-review-view__body-text']")

        def __init__(self, el):
            self.node = el

        @property
        def created_at(self):
            try:
                return self.node.find_element(*self._created_at_locator).get_attribute("content")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def name(self):
            try:
                return self.node.find_element(*self._name_locator).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def stars(self):
            return len(self.node.find_elements(*self._stars_locator))

        @property
        def text(self):
            try:
                return self.node.find_element(*self._text_locator).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return None


def prepare(company_id):
    company = Company.objects.get(pk=company_id)

    if company.parser_link_yandex.startswith("https://yandex.ru/maps/-/"):
        return

    web_driver = driver()
    web_driver.get(company.parser_link_yandex)
    start_page = StartPage(web_driver).open_reviews()

    if start_page.url:
        company.parser_link_yandex = start_page.url
        company.save(update_fields=["parser_link_yandex"])

    web_driver.quit()


def parse(company_id, task):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_yandex = True
    company.save(update_fields=["is_parser_run_yandex"])

    # Парсинг
    web_driver = driver()

    if not company.parser_link_yandex.startswith("https://yandex.ru/maps/-/"):
        try:
            web_driver.get(company.parser_link_yandex)
            reviews_page = ReviewsPage(web_driver).order_all().show_all()

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

        except Exception as exc:
            logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

    web_driver.quit()

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_yandex = False
    company.is_first_parsing_yandex = False
    company.parser_last_parse_at_yandex = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_yandex", "parser_last_parse_at_yandex", "is_parser_run_yandex"])


def perform(company_id, task):
    prepare(company_id)
    parse(company_id, task)