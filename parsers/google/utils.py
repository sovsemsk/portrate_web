import time

from selenium import webdriver

from .parsers import Parser


class GoogleParser:
    def __init__(self, api_secret, parser_link, last_parse_at=None):
        """
        @param api_secret: Ключ доступа Selenoid
        @param parser_link: Ссылка на катрочку компании
        @param last_parse_at: Дата последнего парсинга
        """

        self.api_secret = api_secret
        self.parser_link = parser_link
        self.last_parse_at = last_parse_at

    def __open_page(self):
        options = webdriver.ChromeOptions()
        options.set_capability("selenoid:options", {"enableVNC": True})

        # http://{self.api_secret}@80.87.109.112:4444/wd/hub
        driver = webdriver.Remote(command_executor=f"http://80.87.109.112:4444/wd/hub", options=options)

        parser = Parser(driver, self.last_parse_at)
        driver.get(self.parser_link)
        return parser

    def parse(self, type_parse="default"):
        """
        Функция получения данных в виде
        @param type_parse: Тип данных, принимает значения:
            default - получает все данные по аккаунту
            company - получает данные по компании
            reviews - получает данные по отчетам
        @return: Данные по запрошенному типу
        """

        result = {}
        page = self.__open_page()
        time.sleep(5)

        try:
            if type_parse == "default":
                result = page.parse_all_data()
            if type_parse == "company":
                result = page.parse_company_info()
            if type_parse == "reviews":
                result = page.parse_reviews()

        except Exception as e:
            print(e)
            return result

        finally:
            page.driver.close()
            page.driver.quit()
            return result
