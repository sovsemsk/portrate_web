import re
from datetime import datetime, timezone
import hashlib
import logging
import time

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from parsers.driver import driver
from resources.models import Company, Review, Service

logger = logging.getLogger(__name__)


class ReviewsPage():
    _close_locator = (By.XPATH, ".//cat-services-cookie-banner//cat-brand-icon")
    _rating_locator = (By.XPATH, ".//cat-brand-filial-rating")
    _review_locator = (By.XPATH, ".//cat-layouts-ugc-list/ul/li/cat-entities-ugc-item")
    _more_locator = (By.XPATH, ".//cat-elements-button[@class='js-cat-elements-button--next']")

    def __init__(self, driver):
        self.driver = driver
        time.sleep(10)

    def click_agree(self):
        self.driver.find_element(*self._close_locator).click()
        return self

    def click_more(self):
        ActionChains(self.driver).move_to_element(self.driver.find_element(*self._more_locator)).perform()
        self.driver.find_element(*self._more_locator).click()
        return self

    def scroll_more(self):
        ActionChains(self.driver).move_to_element(self.driver.find_element(*self._more_locator)).perform()
        return self

    @property
    def rating(self):
        return self.driver.find_element(*self._rating_locator).get_attribute("rating")

    @property
    def reviews(self):
        result = []

        for index, el in enumerate(self.driver.find_elements(*self._review_locator)):
            result.append(self.Review(el, self.driver))

            if index == 99:
                break

        return result


    class Review():
        _created_at_locator = (By.XPATH, ".//cat-brand-ugc-date")
        _name_locator = (By.XPATH, ".//cat-brand-name")
        _stars_locator = (By.XPATH, ".//cat-brand-review-estimation")
        _text_locator = (By.XPATH, ".//div[@itemprop='reviewBody']")

        def __init__(self, el, driver):
            self.node = el
            self.driver = driver

        @property
        def guid(self):
            return self.node.get_attribute("data-id")

        @property
        def created_at(self):
            try:
                return self.node.find_element(*self._created_at_locator).get_attribute("date")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def name(self):
            try:
                return self.node.find_element(*self._name_locator).get_attribute("name")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def stars(self):
            try:
                return self.node.find_element(*self._stars_locator).get_attribute("estimation")
            except (AttributeError, NoSuchElementException):
                return None


        @property
        def text(self):
            try:
                el = self.node.find_element(*self._text_locator)
                self.driver.execute_script("arguments[0].setAttribute('style', 'display:block');", el)
                return el.get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return None


def perform(company_id, task):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_flamp = True
    company.save(update_fields=["is_parser_run_flamp"])

    # Парсинг
    web_driver = driver()

    try:
        web_driver.get(company.parser_link_flamp)
        reviews_page = ReviewsPage(web_driver).click_agree().scroll_more().click_more()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at.replace(", отредактирован", ""), languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars if review.stars else 0}") and company.is_visible_flamp),
                    remote_id=hashlib.md5(f"{review.name}{review.created_at}".encode()).hexdigest(),
                    service=Service.FLAMP,
                    stars=int(review.stars if review.stars else 0),
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except Exception as exc:
                logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

        company.rating_flamp = float(reviews_page.rating.replace(",", ".")) if reviews_page.rating else None
        # company.reviews_count_remote_flamp = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_flamp", "reviews_count_remote_flamp"])

    except IntegrityError:
        pass

    web_driver.quit()

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_flamp = False
    company.is_first_parsing_flamp = False
    company.parser_last_parse_at_flamp = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_flamp", "parser_last_parse_at_flamp", "is_parser_run_flamp"])