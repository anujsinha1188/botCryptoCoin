import hmac
import hashlib
import base64
import json
import time
import requests


class OrderStatusCoin:
    def check_order_status(self, cred, order_id):
        # Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
        key = cred["key"]
        secret = cred["secret"]

        # python3
        secret_bytes = bytes(secret, encoding='utf-8')
        # python2
        # secret_bytes = bytes(secret)

        # Generating a timestamp.
        time_stamp = int(round(time.time() * 1000))

        body = {
            "id": order_id,  # Enter your Order ID here.
            # "client_order_id": "2022.02.14-btcinr_1", # Enter your Client Order ID here.
            "timestamp": time_stamp
        }

        json_body = json.dumps(body, separators=(',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/orders/status"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        # print("Log: data: " + str(data))
        return data
