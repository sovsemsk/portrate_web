import requests


class SearchYandex:

    @staticmethod
    def search(query):
        payload = {
            "apikey": "6556c817-ac54-4e7a-8594-0464aaf8c357",
            "lang": "ru_RU",
            "results": "15",
            "type": "biz",
            "text": query
        }

        result = requests.get("https://search-maps.yandex.ru/v1", params=payload)
        print(result.json().get("features", []))
        try:
            return result.json().get("features", [])
        except:
            return []


class SearchGis:

    @staticmethod
    def search(query):
        payload = {
            "key": "25f0a522-41a4-4fd3-a0cd-8876348867db",
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
            "key": "AIzaSyAAhf8FlUtP2F0QuXev4BNSzLoKFCZd874",
            "language": "ru_RU",
            "query": query
        }

        result = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=payload)

        try:
            return result.json().get("results", [])
        except:
            return []
