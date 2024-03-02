import hashlib
import locale
import time
from datetime import datetime, timezone

from bs4 import BeautifulSoup
from django.db import IntegrityError
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from resources.models import Review, Notification


class GisParser:
    def __init__(self, company):
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})
        self.result = []
        self.company = company
        self.driver = webdriver.Remote(command_executor=f"http://80.87.109.112:4444/wd/hub", options=options)

    def parse(self):
        return self.open_page()

    def open_page(self):
        """ Загрузка страницы, ожидание 5 секунд на загрузку """
        self.driver.get(self.company.gis_parser_link)
        time.sleep(5)

        try:
            self.driver.find_element(By.CLASS_NAME, "_tvxwjf")
            self.parse_rating()
            return ", ".join(self.result)
        except NoSuchElementException:
            self.close_page()
            return "Page not valid for GisParser"

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def scroll_reviews_to_bottom(self, element):
        """ Скроллим список до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        new_element = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")[-1]

        if element == new_element:
            return

        self.scroll_reviews_to_bottom(new_element)

    def parse_rating(self):
        """ Получение названия и рейтинга организации """
        try:
            rating_element = self.driver.find_element(By.CLASS_NAME, "_y10azs")
            rating = float(rating_element.text)
            self.company.gis_rate = rating
            self.result.append("Gis rating parse success")
            self.parse_reviews()

        except NoSuchElementException:
            self.result.append("Gis rating parse error")
            self.close_page()

        self.company.gis_rate_last_parse_at = datetime.now(timezone.utc)
        self.company.save()

    def parse_reviews(self):
        """ Спарсить все отзывы """
        str_reviews_elements = []
        reviews_elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        try:
            self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        except NoSuchElementException:
            pass

        if len(reviews_elements) > 1:
            self.scroll_reviews_to_bottom(reviews_elements[-1])
            reviews_elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        for review_element in reviews_elements:
            str_reviews_elements.append(review_element.get_attribute("innerHTML"))

        self.close_page()

        for str_review_element in str_reviews_elements:
            self.parse_review(str_review_element)

        self.company.gis_reviews_last_parse_at = datetime.now(timezone.utc)
        self.company.save()
        self.result.append("Gis reviews parse success")

    def parse_review(self, str_review_element):
        """ Спарсить данные по отзыву """
        bs_element = BeautifulSoup(str_review_element, "html.parser")
        lxml_element = etree.HTML(str(bs_element))

        try:
            date = lxml_element.xpath(".//div[@class='_4mwq3d']")[0].text
        except:
            date = None

        # @TODO: сделать отмену парсинга отзыва если он не сегодняшний, учесть первый парсинг
        # review_date = datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc).date()
        # now_date = datetime.now(timezone.utc).date()

        try:
            name = lxml_element.xpath(".//span[@class='_16s5yj36']")[0].text
        except:
            name = None

        try:
            try:
                text = lxml_element.xpath(".//a[@class='_1it5ivp']")[0].text
            except:
                text = lxml_element.xpath(".//a[@class='_ayej9u3']")[0].text
        except:
            text = None

        try:
            stars = lxml_element.xpath(".//div[@class='_1fkin5c']/span")
        except:
            stars = []

        try:
            review = Review.objects.create(
                created_at=datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc),
                company=self.company,
                name=name,
                rate=self.calc_review_stars_count(stars),
                remote_id=hashlib.md5(f"{name}{date}".encode()).hexdigest(),
                service=Review.Service.GIS,
                text=text
            )

            if review.rate <= 3:
                Notification.objects.create(
                    company=review.company,
                    initiator=Notification.Initiator.GIS_NEGATIVE_REVIEW,
                    review=review,
                    text=review.text,
                )

        except IntegrityError:
            pass

    @staticmethod
    def calc_review_stars_count(review_stars):
        """ Считаем рейтинг по звездам """
        return float(len(review_stars))

    @staticmethod
    def format_review_date(date_string):
        """ Приводим дату в формат Timestamp """
        if date_string == "сегодня":
            return datetime.now().timestamp()
        else:
            splitted_date_string = date_string.replace(", отредактирован", "").split()
            splitted_date_string[1] = splitted_date_string[1][:3]
            cutted_date_string = " ".join(splitted_date_string) #.replace("мая", "май")
            locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8") # Установка локали для парсинга
            datetime_object = datetime.strptime(cutted_date_string, "%d %b %Y")
            return datetime_object.timestamp()
