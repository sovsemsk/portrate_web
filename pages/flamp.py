import time

import dateparser
from django.db import IntegrityError
from pypom import Page, Region
from selenium.webdriver.common.by import By

from driver import driver, company_id
from resources.models import Company, Review, Service


class FlampReviews(Page):
    _close_locator = (By.XPATH, ".//cat-services-cookie-banner//cat-brand-icon")
    _rating_locator = (By.XPATH, ".//cat-brand-filial-rating")
    _review_locator = (By.XPATH, ".//cat-layouts-ugc-list/ul/li/cat-entities-ugc-item")
    _more_locator = (By.XPATH, ".//cat-elements-button[@class='js-cat-elements-button--next']")

    def click_agree(self):
        self.find_element(*self._close_locator).click()
        return self

    def click_more(self):
        self.find_element(*self._more_locator).click()
        return self

    def scroll_more(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(*self._more_locator))
        return self

    @property
    def loaded(self):
        return self.find_element(*self._close_locator).is_displayed()

    @property
    def rating(self):
        return self.find_element(*self._rating_locator).get_attribute("rating")

    @property
    def reviews(self):
        return [self.Review(self, el) for el in self.find_elements(*self._review_locator)]


    class Review(Region):
        _date_locator = (By.XPATH, ".//meta[@itemProp='dateCreated']")
        _name_locator = (By.XPATH, ".//cat-brand-name")
        _stars_locator = (By.XPATH, ".//cat-brand-review-estimation")
        _text_locator = (By.XPATH, ".//div[@itemprop='reviewBody']")

        @property
        def guid(self):
            return self.root.get_attribute("data-id")

        @property
        def date(self):
            return self.find_element(*self._date_locator).get_attribute("content")

        @property
        def name(self):
            return self.find_element(*self._name_locator).get_attribute("name")

        @property
        def stars(self):
            return self.find_element(*self._stars_locator).get_attribute("estimation")

        @property
        def text(self):
            el = self.find_element(*self._text_locator)
            self.driver.execute_script("arguments[0].setAttribute('style', 'display:block');", el)
            return el.text


def test(driver, company_id):
    company = Company.objects.get(pk=company_id)
    flamp_reviews_page = FlampReviews(driver)
    flamp_reviews_page.URL_TEMPLATE = company.parser_link_flamp

    (
        flamp_reviews_page
        .open()
        .click_agree()
        .scroll_more()
        .click_more()
    )

    time.sleep(20)

    # Запись в бд результатов парсинга
    for review in flamp_reviews_page.reviews:
        try:
            Review.objects.create(
                created_at=dateparser.parse(review.date),
                is_visible=(company.__getattribute__(f"is_visible_{review.stars}") and company.is_visible_flamp),
                remote_id=review.guid,
                service=Service.FLAMP,
                stars=int(review.stars),
                name=review.name,
                text=review.text,
                company_id=company.id,
            )
        except IntegrityError:
            pass

    company.rating_flamp = float(flamp_reviews_page.rating)
    company.save(update_fields=["rating_flamp"])

    assert True