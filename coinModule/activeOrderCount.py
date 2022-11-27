import hmac
import hashlib
import base64
import json
import time
import requests


class ActiveOrderCount:
    def get_active_order_count(self, cred, market):
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
            # "side": "buy", # Toggle between a 'buy' or 'sell' order.
            "market": market,  # Replace 'SNTBTC' with your desired market pair.
            "timestamp": time_stamp
        }

        json_body = json.dumps(body, separators=(',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/orders/active_orders_count"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        # print(data)
        return data
