import hashlib
import re
import time

import dateparser
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ParserYandex:
    def __init__(self, parser_link):
        """ Парсер Яндекс """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})
        self.driver = webdriver.Remote(command_executor=f"http://80.87.109.112:4444/wd/hub", options=options)
        self.driver.get(parser_link)
        time.sleep(1)

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def check_page(self):
        """ Проверка страницы """
        try:
            self.driver.find_element(By.CLASS_NAME, "orgpage-header-view__header")
            return True
        except NoSuchElementException:
            return False

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        try:
            node = self.driver.find_element(By.CLASS_NAME, "business-summary-rating-badge-view__rating")
            return float(".".join(re.findall(r'\d+', node.text)))
        except NoSuchElementException:
            return 0.0

    def parse_reviews(self):
        """ Парсинг отзывов """
        result = []

        # Сортировка по дате
        self.__sort_by_newest__()

        # Сбор нод
        nodes = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        if len(nodes) > 1:
            self.__scroll_reviews_to_bottom__(nodes[-1])

        nodes = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        # Парсинг нод
        for node in nodes:
            result.append(self.__parse_review__(node.get_attribute("innerHTML")))

        return result

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(1)
        new_node = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    def __sort_by_newest__(self):
        try:
            menu_node = self.driver.find_element(By.CLASS_NAME, "rating-ranking-view")
            menu_node.click()
        except:
            pass
        finally:
            time.sleep(1)

        try:
            button_node = self.driver.find_elements(By.CLASS_NAME, "rating-ranking-view__popup-line")[1]
            button_node.click()
        except:
            pass
        finally:
            time.sleep(1)

    @staticmethod
    def __parse_review__(str_node):
        """ Парсинг отзыва """
        bs_node = BeautifulSoup(str_node, "html.parser")
        lxml_node = etree.HTML(str(bs_node))

        try:
            date = lxml_node.xpath(".//meta[@itemprop='datePublished']")[0].get("content")
        except:
            date = None

        try:
            name = lxml_node.xpath(".//span[@itemprop='name']")[0].text
        except:
            name = None

        try:
            text = lxml_node.xpath(".//span[@class='business-review-view__body-text']")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath(".//div[@class='business-rating-badge-view__stars']/span")
        except:
            stars = []

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": ParserYandex.__calc_review_stars_count__(stars),
            "text": text
        }

    @staticmethod
    def __calc_review_stars_count__(review_stars):
        """ Подсчет рейтинга по звездам """
        star_count = 0

        for review_star in review_stars:
            if "_empty" in review_star.get("class"):
                continue

            if "_half" in review_star.get("class"):
                star_count = star_count + 0.5
                continue

            star_count = star_count + 1

        return star_count
