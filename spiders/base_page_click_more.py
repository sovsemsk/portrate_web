import time

from spiders.base_page import BasePage

from selenium.common import TimeoutException, NoSuchElementException

class BasePageClickMore(BasePage):

    def _click_more_(self):
        try:
            self.wait_and_click_element(self._more_location)
            self._click_more_()
            time.sleep(5)

        except (AttributeError, NoSuchElementException):
            return

    def show_all(self):
        self._click_more_()
        return self
