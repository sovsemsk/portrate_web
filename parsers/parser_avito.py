import hashlib
import re
import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By


# import datetime


class ParserAvito:
    def __init__(self, parser_link):
        """ Парсер Яндекс """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "screenResolution": "1280x1024x24",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
        })
        self.driver = webdriver.Remote(command_executor=f"http://9bea7b5c.portrate.io/wd/hub", options=options)
        self.driver.get(parser_link)
        time.sleep(5)
        self.driver.implicitly_wait(5)

    def close_page(self):
        self.driver.close()
        self.driver.quit()

    def parse_rating(self):
        try:
            node = self.driver.find_element(By.XPATH, ".//h2[@data-marker='ratingSummary/rating']")
            return float(node.text.replace(",", "."))
        except (NoSuchElementException, StaleElementReferenceException, TypeError, ValueError):
            return False

    def parse_reviews(self):
        """ Парсинг отзывов """
        reviews = []
        nodes = self.driver.find_elements(By.CLASS_NAME, "style-snippet-E6g8Y")

        if len(nodes) > 0:
            self.__scroll_reviews_to_bottom__()
            container_node = nodes[0].find_element(By.XPATH, "./..")
            lxml_container_node = etree.HTML(container_node.get_attribute("innerHTML"))
            lxml_reviews_nodes = lxml_container_node.xpath(".//div[contains(@class, 'style-snippet-E6g8Y')]")

            for index, lxml_review_node in enumerate(lxml_reviews_nodes):
                reviews.append(self.__parse_review__(index, lxml_review_node))

        return reviews

    def __scroll_reviews_to_bottom__(self):
        """ Скроллинг списка до последнего отзыва """
        try:
            button_node = self.driver.find_element(By.XPATH, ".//button[@data-marker='rating-list/moreReviewsButton']")
            button_node.click()
            time.sleep(5)

            self.__scroll_reviews_to_bottom__()
        except NoSuchElementException:
            return

    def __parse_review__(self, index, lxml_node):
        try:
            date = lxml_node.xpath(f".//p[@data-marker='review({index})/header/subtitle']")[0].text
        except IndexError:
            date = None

        try:
            name = lxml_node.xpath(f".//h5[@data-marker='review({index})/header/title']")[0].text
        except IndexError:
            name = None

        try:
            text = lxml_node.xpath(f".//p[@data-marker='review({index})/text-section/text']")[0].text
        except IndexError:
            text = None

        return {
            "created_at": dateparser.parse(str(date), languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": len(lxml_node.xpath(".//path[@fill='#ffb021']")),
            "text": text
        }