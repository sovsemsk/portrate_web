import time
from dataclasses import asdict
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .helpers import ParserHelper
from .storage import Info, Review


class Parser:
    def __init__(self, driver, last_parse_at=None):
        self.driver = driver
        self.last_parse_at = last_parse_at

    def __scroll_to_bottom(self, elem):
        """
        Скроллим список до последнего отзыва
        :param elem: Последний отзыв в списке
        :param driver: Драйвер undetected_chromedriver
        :return: None
        """

        self.driver.execute_script("arguments[0].scrollIntoView();", elem)
        time.sleep(1)
        new_elem = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")[-1]
        if elem == new_elem:
            return

        self.__scroll_to_bottom(new_elem)

    def __get_data_item(self, elem):
        """
        Спарсить данные по отзыву
        :param elem: Отзыв из списка
        :return: Словарь
        {
            name: str
            icon_href: Union[str, None]
            date: float
            text: str
            stars: float
        }
        """

        try:
            name = elem.find_element(By.XPATH, ".//span[@class='_16s5yj36']").get_attribute('innerHTML')
        except NoSuchElementException:
            name = None

        try:
            icon_href = elem.find_element(By.XPATH, ".//div[@class='_1dk5lq4']").get_attribute("style")
            icon_href = icon_href.split('"')[1]
        except NoSuchElementException:
            icon_href = None

        try:
            date = elem.find_element(By.XPATH, ".//div[@class='_4mwq3d']").get_attribute('innerHTML')
        except NoSuchElementException:
            date = None

        try:
            try:
                text = elem.find_element(By.XPATH, ".//a[@class='_1it5ivp']").get_attribute('innerHTML')
            except:
                text = elem.find_element(By.XPATH, ".//a[@class='_ayej9u3']").get_attribute('innerHTML')
        except NoSuchElementException:
            text = None

        try:
            answer = elem.find_element(By.XPATH, ".//div[@class='_j1il10']").get_attribute('innerHTML')
        except NoSuchElementException:
            answer = None

        try:
            stars = elem.find_elements(By.XPATH, ".//div[@class='_1fkin5c']/span")
            stars = ParserHelper.get_count_star(stars)
        except NoSuchElementException:
            stars = 0

        item = Review(
            name=name,
            icon_href=icon_href,
            date=ParserHelper.form_date(date),
            text=text,
            stars=stars,
            answer=answer,
        )

        return asdict(item)

    def __get_data_campaign(self):
        """
        Получаем данные по компании.
        :return: Словарь данных
        {
            name: str
            rating: float
            count_rating: int
            stars: float
        }
        """

        try:
            name = self.driver.find_element(By.XPATH, ".//h1[@class='_tvxwjf']").text
        except NoSuchElementException:
            name = None

        try:
            rating = self.driver.find_element(By.XPATH, ".//div[@class='_y10azs']").text
            count_rating = self.driver.find_element(By.XPATH, ".//div[@class='_jspzdm']").text
            stars = rating # Кек лол :)

        except NoSuchElementException:
            rating = 0
            count_rating = 0
            stars = 0

        item = Info(
            name=name,
            rating=ParserHelper.format_rating(rating),
            count_rating=ParserHelper.format_rating_count(count_rating),
            stars=ParserHelper.format_rating(stars)
        )

        return asdict(item)

    def __get_data_reviews(self):
        reviews = []

        try:
            self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        except Exception:
            pass

        elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        if len(elements) > 1:
            self.__scroll_to_bottom(elements[-1])
            elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

            for elem in elements:
                review = self.__get_data_item(elem)
                reviews.append(review)

                if self.last_parse_at is not None:
                    created_at = datetime.datetime.fromtimestamp(review["date"], datetime.timezone.utc)

                    if created_at < self.last_parse_at:
                        break

        return reviews

    def __isinstance_page(self):
        try:
            xpath_name = ".//h1[@class='_tvxwjf']"
            name = self.driver.find_element(By.XPATH, xpath_name).text
            return True
        except NoSuchElementException:
            return False

    def parse_all_data(self):
        """
        Начинаем парсить данные.
        :return: Словарь данных
        {
             company_info:{
                    name: str
                    rating: float
                    count_rating: int
                    stars: float
            },
            company_reviews:[
                {
                  name: str
                  icon_href: str
                  date: timestamp
                  text: str
                  stars: float
                }
            ]
        }
        """

        if not self.__isinstance_page():
            return {"error": "Страница не найдена"}

        return {
            "company_info": self.__get_data_campaign(),
            "company_reviews": self.__get_data_reviews(),
        }

    def parse_reviews(self):
        """
        Начинаем парсить данные только отзывы.
        :return: Массив отзывов
        {
            company_reviews:[
                {
                  name: str
                  icon_href: str
                  date: timestamp
                  text: str
                  stars: float
                }
            ]
        }
        """

        if not self.__isinstance_page():
            return {"error": "Страница не найдена"}

        return {"company_reviews": self.__get_data_reviews()}

    def parse_company_info(self):
        """
        Начинаем парсить данные только данные о компании.
        :return: Объект компании
        {
            company_info:
                {
                    name: str
                    rating: float
                    count_rating: int
                    stars: float
                }
        }
        """

        if not self.__isinstance_page():
            return {"error": "Страница не найдена"}

        return {"company_info": self.__get_data_campaign()}
