import hashlib
import re
import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By


class ParserYandex:
    def __init__(self, parser_link):
        """ Парсер Яндекс """
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
            node = self.driver.find_element(By.CLASS_NAME, "business-summary-rating-badge-view__rating")
            return float(".".join(re.findall(r"\d+", node.text)))
        except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
            return False

    def parse_reviews(self):
        """ Парсинг отзывов """
        reviews = []
        nodes = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        if len(nodes) > 0:
            self.__scroll_reviews_to_bottom__(nodes[-1])
            container_node = nodes[0].find_element(By.XPATH, "./..")
            lxml_container_node = etree.HTML(container_node.get_attribute("innerHTML"))
            lxml_reviews_nodes = lxml_container_node.xpath(".//div[contains(@class, 'business-reviews-card-view__review')]")

            for lxml_review_node in lxml_reviews_nodes:
                reviews.append(self.__parse_review__(lxml_review_node))

        return reviews

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)

        new_node = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    def __parse_review__(self, lxml_node):
        try:
            date = lxml_node.xpath(".//meta[@itemprop='datePublished']")[0].get("content")
        except IndexError:
            date = None

        try:
            name = lxml_node.xpath(".//span[@itemprop='name']")[0].text
        except IndexError:
            name = None

        try:
            text = lxml_node.xpath(".//span[contains(@class, 'business-review-view__body-text')]")[0].text
        except IndexError:
            text = None

        return {
            "created_at": dateparser.parse(str(date), languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": len(lxml_node.xpath(".//span[contains(@class, '_full')]")),
            "text": text
        }
