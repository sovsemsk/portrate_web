import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from spiders.base_page_scroll_more import BasePageScrollMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageScrollMore):
    _count_location = (By.XPATH, ".//div[@class='jANrlb ']/div[@class='fontBodySmall']")
    _dropdown_location = (By.XPATH, ".//button[@class='HQzyZ']")
    _rating_location = (By.XPATH, ".//div[@class='jANrlb ']/div[@class='fontDisplayLarge']")
    _review_location = (By.XPATH, ".//div[@class='jftiEf fontBodyMedium ']")
    _sort_location = (By.XPATH, ".//div[@class='fxNQSd' and @data-index='1']")

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

        for el in self.wait_and_find_elements(self._review_location):
            result.append(self.ReviewRegion(el))

            if len(result) >= 100:
                break

        return result

    class ReviewRegion(BaseRegion):
        _created_at_location = (By.XPATH, ".//span[@class='rsqaWe']")
        _stars_location = (By.XPATH, ".//span[@class='hCCjke google-symbols NhBTye elGi1d']")
        _name_location = (By.XPATH, ".//div[@class='d4r55 ']")
        _text_location = (By.XPATH, ".//span[@class='wiI7pd']")

        _expand_location = (By.XPATH, ".//button[@class='w8nwRe kyuRq']")

        @property
        def remote_id(self):
            return self._element.get_attribute("data-review-id")

        @property
        def created_at(self):
            return self.find_element(self._created_at_location).get_attribute("textContent")

        @property
        def name(self):
            return self.find_element(self._name_location).get_attribute("textContent")

        @property
        def stars(self):
            return len(self.find_elements(self._stars_location))

        @property
        def text(self):
            return self.find_element(self._text_location).get_attribute("textContent")
