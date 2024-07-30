import hashlib
import time

import dateparser
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParserZoon:
    def __init__(self, parser_link):
        """ Парсер Zoon """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})
        self.driver = webdriver.Remote(command_executor=f"http://185.85.160.249:4444/wd/hub", options=options)
        self.driver.get(parser_link)
        time.sleep(1)

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def check_page(self):
        """ Проверка страницы """
        try:
            self.driver.find_element(By.CLASS_NAME, "js-heading-rating-container")
            return True
        except:
            return False

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        try:
            rating = self.driver.find_element(By.CLASS_NAME, "js-heading-rating-container")
            node = rating.find_elements(By.CLASS_NAME, "z-text--16")
            return float(node.text)
        except:
            return 0.0

    def parse_reviews(self):
        """ Парсинг отзывов """
        result = []

        # try:
        #     self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        # except:
        #     pass

        # Сбор нод
        nodes = self.driver.find_element(By.XPATH, '//div[@itemprop="review"]')

        if len(nodes) > 1:
            self.__scroll_reviews_to_bottom__(nodes[-1])

        nodes = self.driver.find_element(By.XPATH, '//div[@itemprop="review"]')

        # Парсинг нод
        for node in nodes:
            result.append(self.__parse_review__(node.get_attribute("innerHTML")))

        return result

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(2)

        load_reviews_button = self.driver.find_element(By.CSS_SELECTOR, ".js-show-more")
        # click on button and wait loading
        if bool(load_reviews_button):
            load_reviews_button.click()
            time.sleep(5)

        new_node = self.driver.find_element(By.XPATH, '//div[@itemprop="review"]')[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    @staticmethod
    def __parse_review__(str_node):
        """ Парсинг отзыва """
        bs_node = BeautifulSoup(str_node, "html.parser")
        lxml_node = etree.HTML(str(bs_node))

        try:
            date = lxml_node.xpath(".//div[@class='invisible-links']")[0].text
        except:
            date = None

        try:
            name = lxml_node.xpath('.//span[@itemprop="name"]')[0].text
        except:
            name = None

        try:
            text = lxml_node.xpath(".//span[@class='js-comment-content']")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath('.//div[@data-uitest="personal-mark"]')[0].text
        except:
            stars = None

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": stars,
            "text": text
        }
