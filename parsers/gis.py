import hashlib
import locale
import time
from datetime import datetime, timezone

from django.db import IntegrityError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from resources.models import Company, Notification, Review


class GisParser:
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
        self.driver.get(self.company.gis_parser_link)
        time.sleep(5)

        try:
            self.driver.find_element(By.CLASS_NAME, "_tvxwjf")
            self.parse_rating()
            return ", ".join(self.result)
        except NoSuchElementException:
            self.close_page()
            return "Page not found"

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
            self.company.gis_rate_last_parse_at = datetime.now(timezone.utc)
            self.company.save()

            self.result.append("Rating parse success")
            self.parse_reviews()

        except NoSuchElementException:
            self.result.append("Rating parse success")
            self.close_page()

    def parse_reviews(self):
        """ Спарсить все отзывы """
        reviews_elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

        try:
            self.driver.find_element(By.CLASS_NAME, "_fs4sw2").click()
        except NoSuchElementException:
            pass

        if len(reviews_elements) > 1:
            self.scroll_reviews_to_bottom(reviews_elements[-1])
            reviews_elements = self.driver.find_elements(By.CLASS_NAME, "_11gvyqv")

            for review_element in reviews_elements:
                self.parse_review(review_element)

        self.result.append("Reviews parse success")
        self.close_page()

    def parse_review(self, element):
        """ Спарсить данные по отзыву """

        try:
            date = element.find_element(By.XPATH, ".//div[@class='_4mwq3d']").get_attribute('innerHTML')
        except NoSuchElementException:
            date = None

        # @TODO: сделать отмену парсинга отзыва если он не сегодняшний, учесть первый парсинг
        # review_date = datetime.fromtimestamp(self.format_review_date(date), tz=timezone.utc).date()
        # now_date = datetime.now(timezone.utc).date()

        try:
            name = element.find_element(By.XPATH, ".//span[@class='_16s5yj36']").get_attribute('innerHTML')
        except NoSuchElementException:
            name = None

        try:
            try:
                text = element.find_element(By.XPATH, ".//a[@class='_1it5ivp']").get_attribute('innerHTML')
            except NoSuchElementException:
                text = element.find_element(By.XPATH, ".//a[@class='_ayej9u3']").get_attribute('innerHTML')
        except NoSuchElementException:
            text = None

        try:
            icon_href = element.find_element(By.XPATH, ".//div[@class='_1dk5lq4']").get_attribute("style")
            icon_href = icon_href.split('"')[1]
        except NoSuchElementException:
            icon_href = None

        try:
            stars = element.find_elements(By.XPATH, ".//div[@class='_1fkin5c']/span")
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

        finally:
            self.company.yandex_reviews_last_parse_at = datetime.now(timezone.utc)
            self.company.save()

    @staticmethod
    def calc_review_stars_count(review_stars):
        """ Считаем рейтинг по звездам """
        return float(len(review_stars))

    @staticmethod
    def format_review_date(date_string):
        """ Приводим дату в формат Timestamp """

        splitted_date_string = date_string.replace(", отредактирован", "").split()
        splitted_date_string[1] = splitted_date_string[1][:3]
        cutted_date_string = " ".join(splitted_date_string) #.replace("мая", "май")

        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8") # Установка локали для парсинга
        datetime_object = datetime.strptime(cutted_date_string, "%d %b %Y")

        return datetime_object.timestamp()
