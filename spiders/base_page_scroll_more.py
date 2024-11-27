import time
from typing import NoReturn

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from spiders.base_page import BasePage


class BasePageScrollMore(BasePage):
    def _scroll_more(self, node: WebElement) -> NoReturn:
        self._driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)
        new_nods = self.wait().until(EC.presence_of_all_elements_located(self._review_locator))
        new_node = new_nods[-1]

        if node == new_node or len(new_nods) >= 500:
            return

        self._scroll_more(new_node)

    def show_all(self) -> NoReturn:
        nodes = self.wait().until(EC.presence_of_all_elements_located(self._review_locator))

        if len(nodes) > 0:
            self._scroll_more(nodes[-1])