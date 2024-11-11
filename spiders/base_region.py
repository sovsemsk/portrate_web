"""
Модуль базовой реализации PageObjectModel
"""
from typing import List, NoReturn, Tuple, Union

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BaseRegion:
    """
    Класс базовой реализации PageObjectModel
    """
    def __init__(self, element: WebElement) -> None:
        self._element = element

    def wait(self, timeout: int=10) -> WebDriverWait:
        return WebDriverWait(self._element, timeout)

    def wait_element_visible(self, location: Tuple[str, str], timeout: int=10) -> Union[bool, WebElement]:
        """
        Ожидание видимости элемента и его поиск

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.visibility_of_element_located(location))

    def wait_elements_visible(self, location: Tuple[str, str], timeout: int=10) -> Union[bool, List[WebElement]]:
        """
        Ожидание видимости элементов и их поиск

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.visibility_of_all_elements_located(location))

    def wait_element_invisible(self, location: Tuple[str, str], timeout: int=10) -> bool:
        """
        Ожидание невидимости элемента

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.invisibility_of_element(location))

    def wait_element_clickable(self, location: Tuple[str, str], timeout: int=10) -> Union[bool, WebElement]:
        """
        Ожидание кликабельности элемента и его поиск

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        return self.wait(timeout).until(ec.element_to_be_clickable(location))

    def wait_and_find_element(self, location: Tuple[str, str], timeout: int=10) -> WebElement:
        """
        Ожидание видимости элемента и его поиск

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        try:
            return self.wait_element_visible(location, timeout)
        except TimeoutException:
            raise NoSuchElementException

    def wait_and_find_elements(self, location: Tuple[str, str], timeout: int=10) -> List[WebElement]:
        """
        Ожидание видимости элементов и их поиск

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        try:
            return self.wait(timeout).until(ec.visibility_of_all_elements_located(location))
        except TimeoutException:
            raise NoSuchElementException

    def move_to_element(self, location: Tuple[str, str], timeout: int=10) -> NoReturn:
        """
        Смещение фокуса на элемент

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        ActionChains(self._driver).move_to_element(self.wait_and_find_element(location, timeout)).perform()

    def wait_and_click_element(self, location: Tuple[str, str], timeout: int=10) -> NoReturn:
        """
        Ожидание кликабельности элемента и нажатие на него

        :param location: Кортеж из стратегии (By) и локатора
        :param timeout: Время ожидания, секунды
        """
        self.move_to_element(location, timeout)
        self.wait_element_clickable(location, timeout).click()
