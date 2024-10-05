import hashlib
import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By


class ParserGis:
    def __init__(self, parser_link):
        """ Парсер 2Гис """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "screenResolution": "1280x1024x24",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
        })
        self.driver = webdriver.Remote(command_executor="http://9bea7b5c.portrate.io/wd/hub", options=options)
        self.driver.get(parser_link)
        time.sleep(5)
        self.driver.implicitly_wait(5)

    def close_page(self):
        self.driver.close()
        self.driver.quit()

    def parse_rating(self):
        try:
            node = self.driver.find_element(By.CLASS_NAME, "_y10azs")
            return float(node.text)
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def parse_reviews(self):
        reviews = []
        nodes = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        if len(nodes) > 0:
            self.__scroll_reviews_to_bottom__(nodes[-1])
            container_node = nodes[0].find_element(By.XPATH, "./..")
            lxml_container_node = etree.HTML(container_node.get_attribute("innerHTML"))
            lxml_reviews_nodes = lxml_container_node.xpath(".//div[contains(@class, '_11gvyqv')]")

            for lxml_review_node in lxml_reviews_nodes:
                reviews.append(self.__parse_review__(lxml_review_node))

        return reviews

    def __scroll_reviews_to_bottom__(self, node):
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)

        new_node = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    @staticmethod
    def __parse_review__(lxml_node):
        try:
            date = lxml_node.xpath(".//div[contains(@class, '_139ll30')]")[0].text
        except IndexError:
            date = None

        try:
            try:
                name = lxml_node.xpath(".//span[contains(@class, '_16s5yj36')]")[0].text
            except IndexError:
                name = lxml_node.xpath(".//span[contains(@class, '_k6nyhb6')]")[0].text
        except IndexError:
            name = None

        try:
            try:
                text = lxml_node.xpath(".//a[contains(@class, '_h3pmwn')]")[0].text
            except IndexError:
                text = lxml_node.xpath(".//a[contains(@class, '_1oir7fah')]")[0].text
        except IndexError:
            text = None

        return {
            "created_at": dateparser.parse(str(date).replace(", отредактирован", ""), languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": len(lxml_node.xpath(".//div[contains(@class, '_1fkin5c')]/span")),
            "text": text
        }