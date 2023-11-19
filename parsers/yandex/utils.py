import time
from selenium import webdriver


from .parsers import Parser


class YandexParser:
    def __init__(self, api_secret: str, yandex_id: int):
        """
        @param yandex_id: ID Яндекс компании
        """
        self.api_secret = api_secret
        self.yandex_id = yandex_id


    def __open_page(self):
        url: str = 'https://yandex.ru/maps/org/{}/reviews/'.format(str(self.yandex_id))

        options = webdriver.ChromeOptions()
        options.set_capability('selenoid:options', {'enableVNC': True})

        # http://{self.api_secret}@80.87.109.112:4444/wd/hub
        driver = webdriver.Remote(
            command_executor=f'http://80.87.109.112:4444/wd/hub',
            options=options
        )

        parser = Parser(driver)
        driver.get(url)
        return parser


    def parse(self, type_parse: str = 'default') -> dict:
        """
        Функция получения данных в виде
        @param type_parse: Тип данных, принимает значения:
            default - получает все данные по аккаунту
            company - получает данные по компании
            reviews - получает данные по отчетам
        @return: Данные по запрошенному типу
        """
        result:dict = {}
        page = self.__open_page()
        time.sleep(4)
        try:
            if type_parse == 'default':
                result = page.parse_all_data()
            if type_parse == 'company':
                result = page.parse_company_info()
            if type_parse == 'reviews':
                result = page.parse_reviews()
        except Exception as e:
            print(e)
            return result
        finally:
            page.driver.close()
            page.driver.quit()
            return result
        
        