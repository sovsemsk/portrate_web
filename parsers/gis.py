from datetime import datetime, timezone
import hashlib
import logging
import time

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from parsers.driver import driver
from resources.models import Company, Review, Service

logger = logging.getLogger(__name__)


class StartPage():
    _tab_locator = (By.XPATH, ".//div[@class='_1kmhi0c' and .//a[contains(text(), 'Отзывы')]]")
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
    _rating_locator = (By.XPATH, ".//div[@class='_13nm4f0']")
    _count_locator = (By.XPATH, ".//div[@class='_1kmhi0c'][3]//span[@class='_1xhlznaa']")
    _review_locator = (By.XPATH, ".//div[@class='_1k5soqfl']")

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
        time.sleep(5)

        if len(nodes) > 0:
            self._scroll_more_(nodes[-1])

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
        _created_at_locator = (By.XPATH, ".//div[@class='_139ll30']")
        _stars_locator = (By.XPATH, ".//div[@class='_1fkin5c']/span")
        _name_locator = ((By.XPATH, ".//span[@class='_16s5yj36']"), (By.XPATH, ".//span[@class='_k6nyhb6']"))
        _text_locator = ((By.XPATH, ".//a[@class='_h3pmwn']"), (By.XPATH, ".//a[@class='_1oir7fah']"))

        def __init__(self, el):
            self.node = el

        @property
        def created_at(self):
            try:
                return self.node.find_element(*self._created_at_locator).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def stars(self):
            return len(self.node.find_elements(*self._stars_locator))

        @property
        def name(self):
            try:
                return self.node.find_element(*self._name_locator[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self.node.find_element(*self._name_locator[1]).get_attribute("textContent")

        @property
        def text(self):
            try:
                return self.node.find_element(*self._text_locator[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self.node.find_element(*self._text_locator[1]).get_attribute("textContent")


def prepare(company_id):
    company = Company.objects.get(pk=company_id)

    if not company.parser_link_gis.startswith("https://go.2gis.com/"):
        return

    web_driver = driver()
    web_driver.get(company.parser_link_gis)
    start_page = StartPage(web_driver).open_reviews()

    if start_page.url:
        company.parser_link_gis = start_page.url
        company.save(update_fields=["parser_link_gis"])

    web_driver.quit()


def parse(company_id, task):
    company = Company.objects.get(pk=company_id)

    if not (
        company.parser_link_gis.startswith("https://go.2gis.com/") or
        company.parser_link_gis.startswith("https://go.2gis.ru/")
    ):

        # Запись в бд флагов начала парсинга
        company.is_parser_run_gis = True
        company.save(update_fields=["is_parser_run_gis"])

        # Парсинг
        web_driver = driver()

        try:
            web_driver.get(company.parser_link_gis)
            reviews_page = ReviewsPage(web_driver).show_all()

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
                except IntegrityError:
                    pass

            company.rating_gis = float(reviews_page.rating) if reviews_page.rating else None
            company.reviews_count_remote_gis = int(reviews_page.count) if reviews_page.count else None
            company.save(update_fields=["rating_gis", "reviews_count_remote_gis"])

        except Exception as exc:
            logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

        web_driver.quit()

        # Запись в бд флагов окончания парсинга
        company.is_parser_run_gis = False
        company.is_first_parsing_gis = False
        company.parser_last_parse_at_gis = datetime.now(timezone.utc)
        company.save(update_fields=["is_first_parsing_gis", "parser_last_parse_at_gis", "is_parser_run_gis"])


def perform(company_id, task):
    prepare(company_id)
    parse(company_id, task)