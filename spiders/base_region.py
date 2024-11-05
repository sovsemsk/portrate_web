"""
Модуль базовой реализации PageObjectModel
"""
from typing import NoReturn, Tuple, List

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BaseRegion:
    """
    Класс базовой реализации PageObjectModel
    """
    def __init__(self, element: WebElement) -> NoReturn:
        self._element = element

    def wait(self, timeout: int=10) -> WebDriverWait:
        return WebDriverWait(self.element, timeout)

    def find_element(self, location: Tuple[str, str], timeout: int=10) -> WebElement:
        """
        Ожидание видимости элемента и его возврат

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.visibility_of_element_located(location))

    def find_elements(self, location: Tuple[str, str], timeout: int=10) -> List[WebElement]:
        """
        Ожидание видимости элементов и его возврат

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.presence_of_all_elements_located(location))

    def move_to_element(self, location: Tuple[str, str], timeout: int=10) -> NoReturn:
        """
        Смещение фокуса на элемент

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        ActionChains(self._driver).move_to_element(self.find_element(location, timeout)).perform()

    def click_element(self, location: Tuple[str, str], timeout: int=10) -> NoReturn:
        """
        Ожидание кликабельности элемента и нажатие на него

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        self.move_to_element(location)
        self.wait(timeout).until(ec.element_to_be_clickable(location)).click()
