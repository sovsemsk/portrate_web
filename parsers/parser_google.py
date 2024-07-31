import time

import dateparser
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
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
        time.sleep(5)
        self.driver.implicitly_wait(5)

    def close_page(self):
        self.driver.close()
        self.driver.quit()

    def open_reviews_tab(self):
        try:
            self.driver.find_elements(By.CLASS_NAME, "hh2c6")[1].click()
            return True
        except (NoSuchElementException, IndexError):
            return False

    def parse_rating(self):
        try:
            node = self.driver.find_element(By.CLASS_NAME, "fontDisplayLarge")
            return float(node.text.replace(",", "."))
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def parse_reviews(self):
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

    def __scroll_reviews_to_bottom__(self, node):
        self.driver.execute_script("arguments[0].scrollIntoView();", node)

        time.sleep(5)
        new_node = self.driver.find_elements(By.CLASS_NAME, "jftiEf")[-1]

        if node == new_node:
            return

        self.__scroll_reviews_to_bottom__(new_node)

    def __expand_reviews__(self):
        links = self.driver.find_elements(By.CLASS_NAME, 'w8nwRe')

        for link in links:
            link.click()

    def __parse_review__(self, lxml_node):
        try:
            date = lxml_node.xpath(".//span[contains(@class, 'rsqaWe')]")[0].text
        except IndexError:
            date = None

        try:
            name = lxml_node.xpath(".//div[contains(@class, 'd4r55')]")[0].text
        except IndexError:
            name = None

        try:
            text = lxml_node.xpath(".//span[contains(@class, 'wiI7pd')]")[0].text
        except IndexError:
            text = None

        return {
            "created_at": dateparser.parse(date, languages=["ru", "en"]),
            "name": name,
            "remote_id": lxml_node.get("data-review-id"),
            "stars": len(lxml_node.xpath(".//span[contains(@class, 'elGi1d')]")),
            "text": text
        }