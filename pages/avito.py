import re
from datetime import datetime, timezone
import hashlib
import logging
import time

import dateparser
from django.db import IntegrityError
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.driver import driver
from resources.models import Company, Review, Service

logger = logging.getLogger(__name__)


class ReviewsPage():
    _rating_locator = (By.XPATH, ".//h2[@data-marker='ratingSummary/rating']")
    _count_locator = (By.XPATH, ".//p[@data-marker='ratingSummary/description']")
    _review_locator = (By.XPATH, ".//div[@class='style-snippet-E6g8Y']")
    _more_locator = (By.XPATH, ".//button[@data-marker='rating-list/moreReviewsButton']")

    def __init__(self, driver):
        self.driver = driver
        self._wait_first_review_()

    def _wait_first_review_(self):
        review = None
        now = time.time()

        while not review:
            try:
                review = self.driver.find_element(*self._review_locator)

                if time.time() - now > 20:
                    review = True

            except NoSuchElementException:
                continue


    def _click_more_(self):

        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(*self._more_locator))
            time.sleep(10)
            self.driver.find_element(*self._more_locator).click()
            time.sleep(5)
            self._click_more_()
        except (AttributeError, NoSuchElementException):
            return

    def show_all(self):
        self._click_more_()
        return self

    @property
    def rating(self):
        try:
            return self.driver.find_element(*self._rating_locator).get_attribute("textContent")
        except NoSuchElementException:
            return None

    @property
    def count(self):
        try:
            return self.driver.find_element(*self._count_locator).get_attribute("textContent")
        except NoSuchElementException:
            return None

    @property
    def reviews(self):
        result = []

        for index, el in enumerate(self.driver.find_elements(*self._review_locator)):
            result.append(self.Review(el, index))

            if index == 99:
                break

        return result


    class Review():
        def __init__(self, el, index):
            self.node = el
            self.index = index

            self._created_at_locator = (By.XPATH, f".//p[@data-marker='review({index})/header/subtitle']")
            self._name_locator = (By.XPATH, f".//h5[@data-marker='review({index})/header/title']")
            self._stars_locator = (By.XPATH, f".//div[@data-marker='review({index})/score']//*[local-name() = 'path' and @fill='#ffb021']")
            self._text_locator = (By.XPATH, f".//p[@data-marker='review({index})/text-section/text']")

        @property
        def created_at(self):
            return self.node.find_element(*self._created_at_locator).get_attribute("textContent")

        @property
        def stars(self):
            return len(self.node.find_elements(*self._stars_locator))

        @property
        def name(self):
            return self.node.find_element(*self._name_locator).get_attribute("textContent")

        @property
        def text(self):
            text_els = self.node.find_elements(*self._text_locator)

            if len(text_els) == 1:
                text = text_els[0].get_attribute("textContent")
            elif len(text_els) > 1:
                text = f"Преимущества: {text_els[0].get_attribute('textContent')}. Недостатки: {text_els[1].get_attribute('textContent')}"
            else:
                text = None

            return text

def perform(company_id, task):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_avito = True
    company.save(update_fields=["is_parser_run_avito"])

    # Парсинг
    web_driver = driver()

    try:
        web_driver.get(company.parser_link_avito)
        reviews_page = ReviewsPage(web_driver).show_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at.replace(", отредактирован", ""), languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_avito),
                    remote_id=hashlib.md5(f"{review.name}{review.created_at}".encode()).hexdigest(),
                    service=Service.AVITO,
                    stars=review.stars,
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except IntegrityError:
                pass

        company.rating_avito = float(reviews_page.rating.replace(",", ".")) if reviews_page.rating else None
        company.reviews_count_remote_avito = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_avito", "reviews_count_remote_avito"])

    except Exception as exc:
        logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

    web_driver.quit()

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_avito = False
    company.is_first_parsing_avito = False
    company.parser_last_parse_at_avito = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_avito", "parser_last_parse_at_avito", "is_parser_run_avito"])
