import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from spiders.base_page_click_more import BasePageClickMore
from spiders.base_region import BaseRegion


class ReviewsPage(BasePageClickMore):
    _more_location = (By.XPATH, ".//button[@data-qa='show_more_list_items']")

    @property
    def reviews(self):
        return []