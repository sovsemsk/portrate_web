import hashlib
import time

import dateparser
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


# import datetime


class ParserAvito:
    def __init__(self, parser_link):
        """ Парсер Авито """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "screenResolution": "1280x1024x24"
        })
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
            # better find_by data-marker="profile/score"
            self.driver.find_element(By.CLASS_NAME, "desktop-1m2m2bk")
            return True
        except:
            return False

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        try:
            # better find_by data-marker="profile/score"
            node = self.driver.find_element(By.CLASS_NAME, "desktop-1m2m2bk")
            return float(node.text)
        except:
            return 0.0

    def parse_reviews(self):
        """ Парсинг отзывов """
        result = []

        try:
            self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        except:
            pass

        # Сбор нод
        nodes = self.driver.find_elements(By.CLASS_NAME, "style-snippet-E6g8Y")

        if len(nodes) > 1:
            self.__scroll_reviews_to_bottom__(nodes[-1])

        nodes = self.driver.find_elements(By.CLASS_NAME, "style-snippet-E6g8Y")

        # Парсинг нод
        for node in nodes:
            result.append(self.__parse_review__(node.get_attribute("innerHTML")))

        return result

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(2)

        new_node = self.driver.find_elements(By.CLASS_NAME, "style-snippet-E6g8Y")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    @staticmethod
    def __parse_review__(str_node):
        """ Парсинг отзыва """
        bs_node = BeautifulSoup(str_node, "html.parser")
        lxml_node = etree.HTML(str(bs_node))

        try:
            # better find by data-marker="review(0)/header/subtitle"
            date = lxml_node.xpath(".//span[@class='desktop-11ffzh3']")[0].text
            # if date == '28 января':
            #     date = date + datetime.now().year
            # else:
            #     today = datetime.date.today()
            #     months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
            #     if date == 'Сегодня':
            #         date = today.day + months[today.month] + today.year
            #     elif date == 'Вчера':
            #         yesterday = today - timedelta(days=1)
            #         date = yesterday.day + months[yesterday.month] + yesterday.year
            #     else:
            #         date = date
        except:
            date = None

        try:
            # better find by data-marker="review(0)/header/title"
            name = lxml_node.xpath(".//span[@class='desktop-fzlb6d']")[0].text
        except:
            name = None

        try:
            # try:
                comment = lxml_node.xpath(".//div[@class='TextSection-root-Gf13z ReviewBody-text-section-tzVXe']")[0]
                # better find by data-marker="review(1)/text-section/text"
                text = comment.xpath(".//span[@class='desktop-rkrl0v']")[0].text
            # except:
            #     text = lxml_node.xpath(".//a[@class='_ayej9u3']")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath(".//div[@class='Icon-root-_l3uz Attributes-yellow-star-PY9XT']")
        except:
            stars = []

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": hashlib.md5(f"{name}{date}".encode()).hexdigest(),
            "stars": float(len(stars)),
            "text": text
        }
