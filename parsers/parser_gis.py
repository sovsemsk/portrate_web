import hashlib
import time

import dateparser
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParserGis:
    def __init__(self, parser_link):
        """ Парсер 2Гис """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})
        self.driver = webdriver.Remote(command_executor=f"http://185.85.160.249:4444/wd/hub", options=options)
        self.driver.get(parser_link)
        time.sleep(5)

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def check_page(self):
        """ Проверка страницы """
        try:
            self.driver.find_element(By.CLASS_NAME, "_y10azs")
            return True
        except:
            return False

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        try:
            node = self.driver.find_element(By.CLASS_NAME, "_y10azs")
            return float(node.text)
        except:
            return 0.0

    def parse_reviews(self):
        """ Парсинг отзывов """
        result = []

        try:
            self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        except:
            ...

        # Сбор нод
        nodes = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        if len(nodes) > 1:
            self.__scroll_reviews_to_bottom__(nodes[-1])

        nodes = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        # Парсинг нод
        for node in nodes:
            result.append(self.__parse_review__(node.get_attribute("innerHTML")))

        return result

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(2.5)

        new_node = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    @staticmethod
    def __parse_review__(str_node):
        """ Парсинг отзыва """
        bs_node = BeautifulSoup(str_node, "html.parser")
        lxml_node = etree.HTML(str(bs_node))

        try:
            date = lxml_node.xpath(".//div[@class='_4mwq3d']")[0].text
        except:
            date = None

        try:
            name = lxml_node.xpath(".//span[@class='_16s5yj36']")[0].text
        except:
            name = None

        try:
            try:
                text = lxml_node.xpath(".//a[@class='_1it5ivp']")[0].text
            except:
                text = lxml_node.xpath(".//a[@class='_ayej9u3']")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath(".//div[@class='_1fkin5c']/span")
        except:
            stars = []

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": float(len(stars)),
            "text": text
        }
