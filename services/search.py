import requests

from django.conf import settings

class SearchYandex:

    @staticmethod
    def search(query):
        payload = {
            "apikey": settings.YANDEX_API_KEY,
            "lang": "ru_RU",
            "results": "15",
            "type": "biz",
            "text": query
        }

        result = requests.get("https://search-maps.yandex.ru/v1", params=payload)

        try:
            return result.json().get("features", [])
        except:
            return []


class SearchGis:

    @staticmethod
    def search(query):
        payload = {
            "key":  settings.GIS_API_KEY,
            "fields": "items.org",
            "type": "branch",
            "q": query
        }

        result = requests.get("https://catalog.api.2gis.com/3.0/items", params=payload)

        try:
            return result.json().get("result", []).get("items", [])
        except:
            return []


class SearchGoogle:

    @staticmethod
    def search(query):
        payload = {
            "key":  settings.GOOGLE_API_KEY,
            "language": "ru_RU",
            "query": query
        }

        result = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=payload)

        try:
            return result.json().get("results", [])
        except:
            return []
