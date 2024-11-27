"""
Модуль базовой реализации PageObjectModel
"""
from typing import List, NoReturn, Tuple, Union

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
    Класс базовой реализации PageObjectModel
    """
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def wait(self, timeout: int=10) -> WebDriverWait:
        return WebDriverWait(self._driver, timeout)
