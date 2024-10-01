import hashlib
import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)

from selenium.webdriver.common.by import By


class ParserZoon:
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
            self.driver.find_element(By.XPATH, ".//button[contains(text(), 'Мне исполнилось 18 лет')]").click()
        except (AttributeError, NoSuchElementException, StaleElementReferenceException):
            ...

        try:
            node = self.driver.find_element(By.XPATH, ".//div[@data-uitest='stars-count']")
            return float(node.text.replace(",", "."))
        except (AttributeError, NoSuchElementException, StaleElementReferenceException):
            return False

    def parse_reviews(self):
        """ Парсинг отзывов """
        reviews = []
        nodes = self.driver.find_elements(By.XPATH, ".//li[@data-type='comment']")

        if len(nodes) > 0:
            self.__scroll_reviews_to_bottom__()
            container_node = self.driver.find_element(By.XPATH, ".//ul[@data-uitest='org-reviews-list']")

            lxml_container_node = etree.HTML(container_node.get_attribute("innerHTML"))
            lxml_reviews_nodes = lxml_container_node.xpath(".//li[@data-type='comment']")

            for lxml_review_node in lxml_reviews_nodes:
                reviews.append(self.__parse_review__(lxml_review_node))

        return reviews

    def __scroll_reviews_to_bottom__(self):
        """ Скроллинг списка до последнего отзыва """
        try:
            button_show_more = self.driver.find_element(By.CLASS_NAME, "js-show-more")
            self.driver.execute_script(f"window.scrollBy(0,{button_show_more.get_attribute('offsetTop')});")
            time.sleep(5)

            button_show_more.click()
            time.sleep(15)

            self.__scroll_reviews_to_bottom__()
        except (AttributeError, ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException):
            return

    def __parse_review__(self, lxml_node):
        try:
            date = lxml_node.xpath(f".//meta[@itemprop='datePublished']")[0].get("content")
        except IndexError:
            date = None

        try:
            text = lxml_node.xpath(".//span[contains(@class, 'js-comment-content')]")[0].text
        except IndexError:
            text = None

        try:
            stars = lxml_node.xpath(".//meta[@itemprop='ratingValue']")[0].get("content")
        except IndexError:
            stars = 0

        return {
            "created_at": dateparser.parse(str(date), languages=["ru", "en"]),
            "name": lxml_node.get("data-author"),
            "remote_id": lxml_node.get("data-id"),
            "stars": int(stars),
            "text": text
        }