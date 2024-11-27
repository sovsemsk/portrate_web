import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from spiders.base_page_scroll_more import BasePageScrollMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageScrollMore):
    _count_locator = (By.XPATH, ".//div[@class='business-reviews-card-view__title']//h2")
    _dropdown_locator = (By.XPATH, ".//div[@class='rating-ranking-view']")
    _rating_locator = (By.XPATH, ".//div[@class='business-summary-rating-badge-view__rating']")
    _review_locator = (By.XPATH, ".//div[@class='business-reviews-card-view__review']")
    _sort_locator = (By.XPATH, ".//div[@aria-label='По новизне']")

    @property
    def rating(self):
        return self.wait().until(EC.presence_of_element_located(self._rating_locator)).get_attribute("textContent")

    @property
    def count(self):
        return self.wait().until(EC.presence_of_element_located(self._count_locator)).get_attribute("textContent")

    def order_all(self):
        self.wait().until(EC.element_to_be_clickable(self._dropdown_locator)).click()
        self.wait().until(EC.element_to_be_clickable(self._sort_locator)).click()
        time.sleep(5)

    @property
    def reviews(self):
        result = []

        for element in self.wait().until(EC.presence_of_all_elements_located(self._review_locator)):
            result.append(self.ReviewRegion(element))

            if len(result) >= 100:
                break

        return result

    class ReviewRegion(BaseRegion):
        _created_at_locator = (By.XPATH, ".//span[@class='business-review-view__date']")
        _stars_locator = (By.XPATH, ".//span[@class='inline-image _loaded icon business-rating-badge-view__star _full']")
        _name_locator = (By.XPATH, ".//span[@itemprop='name']")
        _text_locator = (By.XPATH, ".//span[@class='business-review-view__body-text']")

        @property
        def created_at(self):
            return self._element.find_element(*self._created_at_locator).get_attribute("textContent")

        @property
        def name(self):
            return self._element.find_element(*self._name_locator).get_attribute("textContent")

        @property
        def stars(self):
            return len(self._element.find_elements(*self._stars_locator))

        @property
        def text(self):
            return self._element.find_element(*self._text_locator).get_attribute("textContent")
