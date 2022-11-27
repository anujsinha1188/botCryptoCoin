import hmac
import hashlib
import base64
import json
import time
import requests


class OrderCoin:
    def run_order(self, cred, side, market, price_per_unit, total_quantity):

        print("Info: Run for " + side + " order.")
        print("market: " + market + ". Price : " + str(price_per_unit) + ". Quantity: " + str(total_quantity))

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
            "side": side,  # Toggle between 'buy' or 'sell'.
            "order_type": "limit_order",  # Toggle between a 'market_order' or 'limit_order'.
            "market": market,  # Replace 'SNTBTC' with your desired market pair.
            "price_per_unit": price_per_unit,  # This parameter is only required for a 'limit_order'
            "total_quantity": total_quantity,  # Replace this with the quantity you want
            "timestamp": time_stamp
        }

        json_body = json.dumps(body, separators=(',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/orders/create"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        print("Info: Response data: " + str(data))
        return data
