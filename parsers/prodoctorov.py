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
    _rating_locator = (By.XPATH, ".//h2[@data-marker='ratingSummary/rating']")
    _count_locator = (By.XPATH, ".//span[@data-qa=['lpu_card_stars_text']")
    _review_locator = (By.XPATH, ".//div[@itemprop='review']")
    _more_locator = (By.XPATH, ".//button[@data-qa='show_more_list_items']")

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
        except:
            return

    def show_all(self):
        self._click_more_()
        return self

    @property
    def rating(self):
        return 5

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
        def __init__(self, el):
            self.node = el

            self._created_at_locator = (By.XPATH, ".//div[@itemprop='datePublished']")
            self._name_locator = (By.XPATH, ".//div[@data-qa='patient_profile__node_author_link']")
            self._stars_locator = (By.XPATH, ".//div[@class='review-card-tooltips__stars review-card-tooltips__stars_positive']/span[@class='ui-text ui-text_subtitle-2 ui-kit-color-text ml-1']"  )
            self._text_locator = (By.XPATH, ".//div[@class='b-review-card__comment-wrapper']")

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
                return self.node.find_element(*self._name_locator).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return None

        @property
        def text(self):
            text_els = self.node.find_elements(*self._text_locator)

            if len(text_els) == 1:
                text = text_els[0].get_attribute("textContent")
            elif len(text_els) > 1:
                text = ""

                try:
                    text += text_els[0].get_attribute('textContent')
                except (AttributeError, IntegrityError):
                    pass

                try:
                    text += text_els[1].get_attribute('textContent')
                except (AttributeError, IntegrityError):
                    pass

                try:
                    text += text_els[2].get_attribute('textContent')
                except (AttributeError, IntegrityError):
                    pass

            else:
                text = None

            return text

def perform(company_id, task=None):
    company = Company.objects.get(pk=company_id)

    # Запись в бд флагов начала парсинга
    company.is_parser_run_prodoctorov = True
    company.save(update_fields=["is_parser_run_prodoctorov"])

    # Парсинг
    web_driver = driver()

    try:
        web_driver.get(company.parser_link_prodoctorov)
        reviews_page = ReviewsPage(web_driver) #.show_all()

        for review in reviews_page.reviews:
            try:
                Review.objects.create(
                    created_at=dateparser.parse(review.created_at.replace(", отредактирован", ""), languages=["ru", "en"]),
                    is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_prodoctorov),
                    remote_id=hashlib.md5(f"{review.name}{review.created_at}".encode()).hexdigest(),
                    service=Service.PRODOCTOROV,
                    stars=review.stars,
                    name=review.name,
                    text=review.text,
                    company_id=company.id
                )
            except IntegrityError:
                pass

        company.rating_prodoctorov = float(reviews_page.rating.replace(",", ".")) if reviews_page.rating else None
        company.reviews_count_remote_prodoctorov = int("".join(re.findall(r"\d+", reviews_page.count))) if reviews_page.count else None
        company.save(update_fields=["rating_prodoctorov", "reviews_count_remote_prodoctorov"])

    except Exception as exc:
        logger.exception(f"Task {task.request.task}[{task.request.id}] failed:", exc_info=exc)

    web_driver.quit()

    # Запись в бд флагов окончания парсинга
    company.is_parser_run_prodoctorov = False
    company.is_first_parsing_prodoctorov = False
    company.parser_last_parse_at_prodoctorov = datetime.now(timezone.utc)
    company.save(update_fields=["is_first_parsing_prodoctorov", "parser_last_parse_at_prodoctorov", "is_parser_run_prodoctorov"])
