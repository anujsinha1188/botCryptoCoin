import hmac
import hashlib
import base64
import json
import time
import requests


class AccountTradeHistory:
    def get_account_trade_history(self, cred):
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
            # "from_id": 352622,
            "limit": 1,
            "timestamp": time_stamp,
            "sort": "desc",
            # "from_timestamp": 1514745000000,  # replace this with your from timestamp filter
            # "to_timestamp": 1514745000000,  # replace this with your to timestamp filter
            # "symbol": "BCHBTC"  # replace this with your symbol filter
        }

        json_body = json.dumps(body, separators=(',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/orders/trade_history"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        # print(data)
        return data
