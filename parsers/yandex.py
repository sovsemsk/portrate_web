import hashlib
import re
import time
from datetime import datetime, timezone

from bs4 import BeautifulSoup
from django.db import IntegrityError
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from resources.models import Notification, Review


class YandexParser:
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
        self.driver.get(self.company.yandex_parser_link)
        time.sleep(5)

        try:
            self.driver.find_element(By.CLASS_NAME, "orgpage-header-view__header")
            self.parse_rating()
            return ", ".join(self.result)
        except NoSuchElementException:
            self.close_page()
            return "Page not valid for YandexParser"

    def close_page(self):
        """ Закрытие страницы """
        self.driver.close()
        self.driver.quit()

    def scroll_reviews_to_bottom(self, element):
        """ Скроллим список до последнего отзыва """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        new_element = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]

        if element == new_element:
            return

        self.scroll_reviews_to_bottom(new_element)

    def parse_rating(self):
        """ Получение названия и рейтинга организации """
        try:
            rating_element = self.driver.find_element(By.CLASS_NAME, "business-summary-rating-badge-view__rating")
            rating = float(".".join(re.findall(r'\d+', rating_element.text)))
            self.company.yandex_rate = rating
            # self.company.portrate_rate = (self.company.yandex_rate + self.company.portrate_rate + self.company.gis_rate) / 3
            self.result.append("Yandex rating parse success")
            self.parse_reviews()

        except NoSuchElementException:
            self.result.append("Yandex rating parse error")
            self.close_page()

        self.company.yandex_rate_last_parse_at = datetime.now(timezone.utc)
        self.company.save()

    def parse_reviews(self):
        """ Спарсить все отзывы """
        str_reviews_elements = []
        reviews_elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        if len(reviews_elements) > 1:
            self.scroll_reviews_to_bottom(reviews_elements[-1])
            reviews_elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        for review_element in reviews_elements:
            str_reviews_elements.append(review_element.get_attribute("innerHTML"))

        self.close_page()

        for str_review_element in str_reviews_elements:
            self.parse_review(str_review_element)

        self.company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
        self.company.save()
        self.result.append("Yandex reviews parse success")

    def parse_review(self, str_review_element):
        """ Спарсить данные по отзыву """
        bs_element = BeautifulSoup(str_review_element, "html.parser")
        lxml_element = etree.HTML(str(bs_element))

        try:
            date = lxml_element.xpath(".//meta[@itemprop='datePublished']")[0].get("content")
        except:
            date = None

        # @TODO: сделать отмену парсинга отзыва если он не сегодняшний, учесть первый парсинг
        # review_date = datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc).date()
        # now_date = datetime.now(timezone.utc).date()

        try:
            name = lxml_element.xpath(".//span[@itemprop='name']")[0].text
        except:
            name = None

        try:
            text = lxml_element.xpath(".//span[@class='business-review-view__body-text']")[0].text
        except:
            text = None

        try:
            stars = lxml_element.xpath(".//div[@class='business-rating-badge-view__stars']/span")
        except:
            stars = []

        try:
            review = Review.objects.create(
                created_at=datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc),
                company=self.company,
                name=name,
                rate=self.calc_review_stars_count(stars),
                remote_id=hashlib.md5(f"{name}{date}".encode()).hexdigest(),
                service=Review.Service.YANDEX,
                text=text,
            )

            if review.rate <= 3:
                Notification.objects.create(
                    company=review.company,
                    initiator=Notification.Initiator.YANDEX_NEGATIVE_REVIEW,
                    review=review,
                    text=review.text,
                )

        except IntegrityError:
            pass

    @staticmethod
    def calc_review_stars_count(review_stars):
        """ Считаем рейтинг по звездам """
        star_count = 0

        for review_star in review_stars:
            if "_empty" in review_star.get("class"):
                continue

            if "_half" in review_star.get("class"):
                star_count = star_count + 0.5
                continue

            star_count = star_count + 1

        return star_count

    @staticmethod
    def format_review_date(date_string):
        """ Приводим дату в формат Timestamp """
        datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return datetime_object.timestamp()
