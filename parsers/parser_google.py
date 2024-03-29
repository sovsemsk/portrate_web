import time

import dateparser
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParserGoogle:
    def __init__(self, parser_link):
        """ Парсер Google """
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
            self.driver.find_element(By.XPATH, ".//div[@class='jANrlb ']/div[@class='fontDisplayLarge']")
            return True
        except:
            return False

    def parse_rating(self):
        """ Парсинг рейтинга организации """
        try:
            node = self.driver.find_element(By.XPATH, ".//div[@class='jANrlb ']/div[@class='fontDisplayLarge']")
            return float(node.text.replace(",", "."))
        except:
            return 0.0

    def parse_reviews(self):
        """ Парсинг отзывов """
        result = []

        # Сортировка по дате
        # self.__sort_by_newest__()

        # Сбор нод
        nodes = self.driver.find_elements(By.CLASS_NAME, "jftiEf")

        if len(nodes) > 1:
            self.__scroll_reviews_to_bottom__(nodes[-1])

        nodes = self.driver.find_elements(By.CLASS_NAME, "jftiEf")

        # Раскрытие комментариев
        self.__expand_reviews__()

        # Парсинг нод
        for node in nodes:
            result.append(ParserGoogle.__parse_review__(node.get_attribute("innerHTML")))

        return result

    def __scroll_reviews_to_bottom__(self, node):
        """ Скроллинг списка до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", node)
        time.sleep(5)

        new_node = self.driver.find_elements(By.CLASS_NAME, "jftiEf")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    def __sort_by_newest__(self):
        """ Сортировка по дате создания """
        try:
            menu_node = self.driver.find_element(By.CLASS_NAME, "HQzyZ")
            menu_node.click()
        except:
            pass
        finally:
            time.sleep(5)

        try:
            button_node = self.driver.find_elements(By.CLASS_NAME, "fxNQSd")[1]
            button_node.click()
        except:
            pass
        finally:
            time.sleep(1)

    def __expand_reviews__(self):
        """ Раскрытие комментариев """
        try:
            links = self.driver.find_elements(By.CLASS_NAME, 'w8nwRe')

            for link in links:
                link.click()
        except:
            pass

    @staticmethod
    def __parse_review__(str_node):
        """ Парсинг отзыва """
        bs_node = BeautifulSoup(str_node, "html.parser")
        lxml_node = etree.HTML(str(bs_node))

        try:
            date = lxml_node.xpath(".//span[@class='rsqaWe']")[0].text
        except:
            date = None

        try:
            remote_id = lxml_node.xpath(".//button[@class='al6Kxe']")[0].get("data-review-id")
        except:
            remote_id = None

        try:
            name = lxml_node.xpath(".//div[@class='d4r55']")[0].text
        except:
            name = None

        try:
            text = lxml_node.xpath(".//span[@class='wiI7pd']")[0].text
        except:
            text = None

        try:
            stars = lxml_node.xpath(".//span[@class='hCCjke vzX5Ic google-symbols NhBTye']")
        except:
            stars = []

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": remote_id,
            "stars": float(len(stars)),
            "text": text
        }
