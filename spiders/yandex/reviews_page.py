import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from spiders.base_page_scroll_more import BasePageScrollMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageScrollMore):
    _count_location = (By.XPATH, ".//h2[@class='card-section-header__title _wide']")
    _dropdown_location = (By.XPATH, ".//div[@class='rating-ranking-view']")
    _rating_location = (By.XPATH, ".//div[@class='business-summary-rating-badge-view__rating']")
    _review_location = (By.XPATH, ".//div[@class='business-reviews-card-view__review']")
    _sort_location = (By.XPATH, ".//div[@aria-label='По новизне']")

    @property
    def rating(self):
        return self.wait_and_find_element(self._rating_location).get_attribute("textContent")

    @property
    def count(self):
        return self.wait_and_find_element(self._count_location).get_attribute("textContent")

    def order_all(self):
        self.wait_and_find_element(self._dropdown_location).click()
        self.wait_and_find_element(self._sort_location).click()
        time.sleep(5)
        return self

    @property
    def reviews(self):
        result = []

        for index, el in enumerate(self.wait_and_find_elements(self._review_location)):
            try:
                result.append(self.ReviewRegion(el))
            except (AttributeError, NoSuchElementException):
                pass

            if index == 99:
                break

        return result

    class ReviewRegion(BaseRegion):
        _created_at_location = (By.XPATH, ".//span[@class='business-review-view__date']")
        _stars_location = (By.XPATH, ".//span[@class='inline-image _loaded icon business-rating-badge-view__star _full']")
        _name_location = (By.XPATH, ".//span[@itemprop='name']")
        _text_location = (By.XPATH, ".//span[@class='business-review-view__body-text']")

        @property
        def created_at(self):
            return self.wait_and_find_element(self._created_at_location).get_attribute("textContent")

        @property
        def name(self):
            return self.wait_and_find_element(self._name_location).get_attribute("textContent")

        @property
        def stars(self):
            return len(self.wait_and_find_elements(self._stars_location))

        @property
        def text(self):
            return self.wait_and_find_element(self._text_location).get_attribute("textContent")
