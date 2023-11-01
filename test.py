from src.utils import YandexParser
id_ya = 1234 #ID Компании Yandex
parser = YandexParser(id_ya)

all_data = parser.parse() #Получаем все данные
company = parser.parse(type_parse='company') #Получаем данные по компании
reviews = parser.parse(type_parse='company') #Получаем список отзывов

print(reviews)