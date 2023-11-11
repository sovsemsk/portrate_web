import undetected_chromedriver

from yandex_reviews_parser.parsers import Parser
from yandex_reviews_parser.utils import YandexParser

class YP(YandexParser):
    def __init__(self, id_yandex: int):
        """
        @param id_yandex: ID Яндекс компании
        """
        self.id_yandex = id_yandex

    def __open_page(self):
        url: str = 'https://yandex.ru/maps/org/{}/reviews/'.format(str(self.id_yandex))
        opts = undetected_chromedriver.ChromeOptions()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('headless')
        opts.add_argument('--disable-gpu')
        driver = undetected_chromedriver.Chrome(options=opts)
        parser = Parser(driver)
        driver.get(url)
        return parser






id_ya = 21556448302 #ID Компании Yandex




parser = YP(id_ya)

all_data = parser.parse() #Получаем все данные
company = parser.parse(type_parse='company') #Получаем данные по компании
reviews = parser.parse(type_parse='company') #Получаем список отзывов

print(reviews)