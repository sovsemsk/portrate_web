import re
from datetime import datetime, timezone
import hashlib
import logging
import time

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException, JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from parsers.driver import driver
from resources.models import Company, Review, Service

logger = logging.getLogger(__name__)


class ReviewsPage():
    _close_locator = (By.XPATH, ".//button[text() = 'Мне исполнилось 18 лет']")
    _rating_locator = (By.XPATH, ".//div[@data-uitest='stars-count']")
    _count_locator = (By.XPATH, ".//a[@data-type='reviews']/span[@class='service-block-nav-item-count z-text--13']")
    _review_locator = (By.XPATH, ".//ul[@data-uitest='org-reviews-list']/li[@data-type='comment']")
    _more_locator = (By.XPATH, ".//a[@class='z-button z-button--44 z-button--secondary z-button--fluid js-show-more']")

    def __init__(self, driver):
        self.driver = driver
        time.sleep(10)

    def _click_more_(self):
        try:
            ActionChains(self.driver).move_to_element(self.driver.find_element(*self._more_locator)).perform()
            time.sleep(10)
            self.driver.find_element(*self._more_locator).click()
            time.sleep(5)
            self._click_more_()
        except (AttributeError, NoSuchElementException, JavascriptException):
            return

    def click_agree(self):
        try:
            self.driver.find_element(*self._close_locator).click()
        except:
            pass

        return self

    def show_all(self):
        self._click_more_()
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
        _stars_locator = (By.XPATH, ".//meta[@itemprop='ratingValue']")
        _text_locator = (
            (By.XPATH, "./div/div/div/div/span[contains(@class, 'js-comment-content')]"),
            (By.XPATH, "./div/div/div/div/div/div/span[contains(@class, 'js-comment-content')]")
        )

        def __init__(self, el):
            self.node = el

        @property
        def remote_id(self):
            return self.node.get_attribute("data-id")

        @property
        def created_at(self):
            try:
                return self.node.find_element(*self._created_at_locator).get_attribute("content")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def stars(self):
            try:
                return self.node.find_element(*self._stars_locator).get_attribute("content")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def name(self):
            return self.node.get_attribute("data-author")

        @property
        def text(self):
            try:
                return  self.node.find_element(*self._text_locator[0]).get_attribute("textContent")
            except NoSuchElementException:
                try:
                    text_els = self.node.find_elements(*self._text_locator[1])
                    return f"Преимущества: {text_els[0].get_attribute('textContent')}. Недостатки: {text_els[1].get_attribute('textContent')}. Комментарий: {text_els[2].get_attribute('textContent')}"
                except (AttributeError, IndexError):
                    return None

def perform(company_id, task):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_zoon = True
    company.save(update_fields=["is_parser_run_zoon"])

    # Парсинг
    web_driver = driver()

    try:
        web_driver.get(company.parser_link_zoon)
        reviews_page = ReviewsPage(web_driver).click_agree().show_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at, languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars if review.stars else 0}") and company.is_visible_zoon),
                    remote_id=review.remote_id,
                    service=Service.ZOON,
                    stars=int(review.stars if review.stars else 0),
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except IntegrityError:
                pass

        company.rating_zoon = float(reviews_page.rating.replace(",", ".")) if reviews_page.rating else None
        company.reviews_count_remote_zoon = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_zoon", "reviews_count_remote_zoon"])

    except Exception as exc:
        logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

    web_driver.quit()

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_zoon = False
    company.is_first_parsing_zoon = False
    company.parser_last_parse_at_zoon = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_zoon", "parser_last_parse_at_zoon", "is_parser_run_zoon"])
