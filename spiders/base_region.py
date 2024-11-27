"""
Модуль базовой реализации PageObjectModel
"""
from typing import List, NoReturn, Tuple, Union

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
