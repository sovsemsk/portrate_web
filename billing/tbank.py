import hashlib
import json

import requests
from django.conf import settings


class Tbank():
    tbank_key = settings.TBANK_KEY
    tbank_secret = settings.TBANK_SECRET
    init_url = "https://securepay.tinkoff.ru/v2/Init"

    def create_hash(self, hash_array):
        hash_array["Password"] = self.tbank_secret
        sorted_hash_array = json.loads(json.dumps(hash_array, sort_keys=True))
        hash_string = ""

        for key in sorted_hash_array:
            value = sorted_hash_array[key]
            hash_string += str(value)

        return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()

    def send_request(self, data, url):
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        data["TerminalKey"] = self.tbank_key
        data["Token"] = self.create_hash(data.copy())

        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()

    def init_order(self, order_number, amount):
        data = {"OrderId": str(order_number), "Amount": int(float(amount * 100))}
        return self.send_request(data, self.init_url)