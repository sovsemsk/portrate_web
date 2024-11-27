from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from spiders.base_page_scroll_more import BasePageScrollMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageScrollMore):
    _count_locator = (By.XPATH, ".//div[@class='_1bmk0ql']")
    _rating_locator = (By.XPATH, ".//div[@class='_13nm4f0']")
    _review_locator = (By.XPATH, ".//div[@class='_1k5soqfl']")

    @property
    def rating(self):
        return self.wait().until(EC.presence_of_element_located(self._rating_locator)).get_attribute("textContent")

    @property
    def count(self):
        return self.wait().until(EC.presence_of_element_located(self._count_locator)).get_attribute("textContent")

    @property
    def reviews(self):
        result = []

        for element in self.wait().until(EC.presence_of_all_elements_located(self._review_locator)):
            result.append(self.ReviewRegion(element))

            if len(result) >= 100:
                break

        return result

    class ReviewRegion(BaseRegion):
        _created_at_locator = (By.XPATH, ".//div[@class='_139ll30']")
        _stars_locator = (By.XPATH, ".//div[@class='_1fkin5c']/span")
        _name_locator = ((By.XPATH, ".//span[@class='_16s5yj36']"), (By.XPATH, ".//span[@class='_k6nyhb6']"))
        _text_locator = ((By.XPATH, ".//a[@class='_h3pmwn']"), (By.XPATH, ".//a[@class='_1oir7fah']"))

        @property
        def created_at(self):
            return self._element.find_element(*self._created_at_locator).get_attribute("textContent")

        @property
        def name(self):
            try:
                return self._element.find_element(*self._name_locator[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self._element.find_element(*self._name_locator[1]).get_attribute("textContent")

        @property
        def stars(self):
            return len(self._element.find_elements(*self._stars_locator))

        @property
        def text(self):
            try:
                return self._element.find_element(*self._text_locator[0]).get_attribute("textContent")
            except (AttributeError, NoSuchElementException):
                return self._element.find_element(*self._text_locator[1]).get_attribute("textContent")
