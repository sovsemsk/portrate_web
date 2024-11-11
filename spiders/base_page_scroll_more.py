import time
from typing import Self, NoReturn

from selenium.webdriver.remote.webelement import WebElement

from spiders.base_page import BasePage


class BasePageScrollMore(BasePage):
    def _scroll_more(self, node: WebElement) -> NoReturn:
        review_strategy, review_path = self._review_location
        self.move_to_element((review_strategy, f"{review_path}[last()]"))

        time.sleep(1)

        new_nods = self.wait_and_find_elements(self._review_location)
        new_node = new_nods[-1]

        if node == new_node: # or len(new_nods) >= 500:
            return

        self._scroll_more(new_node)

    def show_all(self) -> Self:
        nodes = self.wait_and_find_elements(self._review_location)

        time.sleep(1)

        if len(nodes) > 0:
            self._scroll_more(nodes[-1])

        return self