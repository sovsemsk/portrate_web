import time
from typing import NoReturn

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from spiders.base_page import BasePage


class BasePageScrollMore(BasePage):
    def _scroll_more(self, node: WebElement) -> NoReturn:
        # _, review_path = self._review_location
        # self.move_to_element((By.XPATH, f"{review_path}[last()]"))

        self._driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)
        new_nods = self.wait_and_find_elements(self._review_location)
        new_node = new_nods[-1]

        if node == new_node or len(new_nods) >= 500:
            return

        self._scroll_more(new_node)

    def show_all(self) -> NoReturn:
        nodes = self.wait_and_find_elements(self._review_location)

        if len(nodes) > 0:
            self._scroll_more(nodes[-1])