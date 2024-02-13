import hashlib
import re
import time
from datetime import datetime, timezone

from django.db import IntegrityError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from resources.models import Company, Notification, Review


class YandexParser:
    def __init__(self, company_id):
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})

        self.result = []
        self.company = Company.objects.get(id=company_id)
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
            return "Yandex page not found"

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
            self.company.yandex_rate_last_parse_at = datetime.now(timezone.utc)
            self.company.save()
            self.result.append("Yandex rating parse success")
            self.parse_reviews()

        except NoSuchElementException:
            self.result.append("Yandex rating parse error")
            self.close_page()

    def parse_reviews(self):
        """ Спарсить все отзывы """
        reviews_elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        if len(reviews_elements) > 1:
            self.scroll_reviews_to_bottom(reviews_elements[-1])
            reviews_elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")

        for review_element in reviews_elements:
            self.parse_review(review_element)

        self.result.append("Reviews parse success")
        self.close_page()

    def parse_review(self, element):
        """ Спарсить данные по отзыву """

        try:
            date = element.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute("content")
        except NoSuchElementException:
            date = None

        # @TODO: сделать отмену парсинга отзыва если он не сегодняшний, учесть первый парсинг
        # review_date = datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc).date()
        # now_date = datetime.now(timezone.utc).date()

        try:
            name = element.find_element(By.XPATH, ".//span[@itemprop='name']").text
        except NoSuchElementException:
            name = None

        try:
            text = element.find_element(By.XPATH, ".//span[@class='business-review-view__body-text']").text
        except NoSuchElementException:
            text = None

        try:
            icon_href = element.find_element(By.XPATH, ".//div[@class='user-icon-view__icon']").get_attribute("style")
            icon_href = icon_href.split('"')[1]
        except NoSuchElementException:
            icon_href = None

        try:
            stars = element.find_elements(By.XPATH, ".//div[@class='business-rating-badge-view__stars']/span")
            stars = stars
        except NoSuchElementException:
            stars = 0

        try:
            review = Review.objects.create(
                avatar_url=icon_href,
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

        finally:
            self.company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
            self.company.save()

    @staticmethod
    def calc_review_stars_count(review_stars):
        """ Считаем рейтинг по звездам """

        star_count = 0

        for review_star in review_stars:
            if "_empty" in review_star.get_attribute("class"):
                continue

            if "_half" in review_star.get_attribute("class"):
                star_count = star_count + 0.5
                continue

            star_count = star_count + 1

        return star_count

    @staticmethod
    def format_review_date(date_string):
        """ Приводим дату в формат Timestamp """

        datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return datetime_object.timestamp()
