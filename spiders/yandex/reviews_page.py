"""
Модуль реализации страницы авторизации в рамках PageObjectModel
"""
from typing import Self

from selenium.webdriver.common.by import By

from spiders.base_page import BasePage


class ReviewsPage(BasePage):
    """
    Класс реализации страницы авторизации в рамках PageObjectModel
    """
    _button_login = (By.XPATH, '//button[contains(@class, "login-btn")]')
    _div_error_message = (By.XPATH, '//div[contains(@class, "error-msg")]')
    _input_login = (By.XPATH, '//input[@ng-model="vm.login"]')
    _input_password = (By.XPATH, '//input[@ng-model="vm.password"]')

    @property
    def loaded(self) -> bool:
        return self.find_element(self._button_login) is not None

    @property
    def div_error_message_text(self) -> str:
        return self.find_element(self._div_error_message).get_attribute("textContent")

    @property
    def input_login_value(self) -> str:
        return self.find_element(self._input_login).get_attribute("value")

    @property
    def input_password_value(self) -> str:
        return self.find_element(self._input_password).get_attribute("value")

    @allure.step('Начало сессии')
    def login(self, login: str, password: str) -> Self:
        self.find_element(self._input_login).send_keys(login)
        self.find_element(self._input_password).send_keys(password)
        self.click_element(self._button_login)
        return self
