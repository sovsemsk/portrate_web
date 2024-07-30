import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParserGoogle:
    def __init__(self, parser_link):
        """ Парсер Google """
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "screenResolution": "1280x1024x24",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
        })
        self.driver = webdriver.Remote(command_executor=f"http://9bea7b5c.portrate.io/wd/hub", options=options)
        self.driver.get(parser_link)
        self.__open_reviews_tab__()
        time.sleep(5)

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        node = self.driver.find_element(By.CLASS_NAME, "fontDisplayLarge")
        return float(node.text.replace(",", "."))

    def parse_reviews(self):
        """ Парсинг отзывов """
        reviews = []
        nodes = self.driver.find_elements(By.CLASS_NAME, "jftiEf")

        if len(nodes) > 0:
            self.__scroll_reviews_to_bottom__(nodes[-1])
            self.__expand_reviews__()
            container_node = nodes[0].find_element(By.XPATH, "./..")
            lxml_container_node = etree.HTML(container_node.get_attribute("innerHTML"))
            lxml_reviews_nodes = lxml_container_node.xpath(".//div[contains(@class, 'jftiEf')]")

            for lxml_review_node in lxml_reviews_nodes:
                review = self.__parse_review__(lxml_review_node)

                if review["text"]:
                    reviews.append(review)

        return reviews

    def __open_reviews_tab__(self):
        """ Переход на страницу отзывов """
        tab_node = self.driver.find_elements(By.CLASS_NAME, "hh2c6")[1]
        tab_node.click()
        time.sleep(5)

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)

        time.sleep(5)
        new_node = self.driver.find_elements(By.CLASS_NAME, "jftiEf")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    def __expand_reviews__(self):
        """ Раскрытие комментариев """
        links = self.driver.find_elements(By.CLASS_NAME, 'w8nwRe')

        for link in links:
            link.click()

    def __sort_by_newest__(self):
        """ Сортировка по дате создания """
        try:
            menu_node = self.driver.find_element(By.CLASS_NAME, "HQzyZ")
            menu_node.click()
        except:
            ...
        finally:
            time.sleep(1)

        try:
            button_node = self.driver.find_elements(By.CLASS_NAME, "fxNQSd")[1]
            button_node.click()
        except:
            ...
        finally:
            time.sleep(1)

    def __parse_review__(self, lxml_node):
        """ Парсинг отзыва """
        try:
            date = lxml_node.xpath(".//span[contains(@class, 'rsqaWe')]")[0].text
        except:
            date = None

        try:
            remote_id = lxml_node.get("data-review-id")
        except:
            remote_id = None

        try:
            name = lxml_node.xpath(".//div[contains(@class, 'd4r55')]")[0].text
        except:
            name = None

        try:
            text = lxml_node.xpath(".//span[contains(@class, 'wiI7pd')]")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath(".//span[contains(@class, 'elGi1d')]")
        except:
            stars = []

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": remote_id,
            "stars": len(stars),
            "text": text
        }