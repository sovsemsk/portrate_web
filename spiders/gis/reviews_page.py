from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from spiders.base_page_scroll_more import BasePageScrollMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageScrollMore):
    _count_location = (By.XPATH, ".//div[@class='_1bmk0ql']")
    _rating_location = (By.XPATH, ".//div[@class='_13nm4f0']")
    _review_location = (By.XPATH, ".//div[@class='_1k5soqfl']")

    @property
    def rating(self):
        return self.wait_and_find_element(self._rating_location).get_attribute("textContent")

    @property
    def count(self):
        return self.wait_and_find_element(self._count_location).get_attribute("textContent")

    @property
    def reviews(self):
        result = []

        for el in self.wait_and_find_elements(self._review_location):
            result.append(self.ReviewRegion(el))

            if len(result) >= 100:
                break

        return result

    class ReviewRegion(BaseRegion):
        _created_at_location = (By.XPATH, ".//div[@class='_139ll30']")
        _stars_location = (By.XPATH, ".//div[@class='_1fkin5c']/span")
        _name_location = ((By.XPATH, ".//span[@class='_16s5yj36']"), (By.XPATH, ".//span[@class='_k6nyhb6']"))
        _text_location = ((By.XPATH, ".//a[@class='_h3pmwn']"), (By.XPATH, ".//a[@class='_1oir7fah']"))

        @property
        def created_at(self):
            return self.find_element(self._created_at_location).get_attribute("textContent")

        @property
        def name(self):
            try:
                return self.find_element(self._name_location[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self.find_element(self._name_location[1]).get_attribute("textContent")

        @property
        def stars(self):
            return len(self.find_elements(self._stars_location))

        @property
        def text(self):
            try:
                return self.find_element(self._text_location[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self.find_element(self._text_location[1]).get_attribute("textContent")
