import json

from coinModule.accountTradeHistory import AccountTradeHistory
from coinModule.activeOrderCount import ActiveOrderCount
from coinModule.orderCoin import OrderCoin
from coinModule.orderStatusCoin import OrderStatusCoin


class CoinService:
    cred = None

    sellCoinFactory = OrderCoin()
    orderStatusFactory = OrderStatusCoin()
    activeOrderCountFactory = ActiveOrderCount()
    accountTradeHistory = AccountTradeHistory()

    credJsonFilePath = "../coinModule/cred.json"

    def get_cred(self):
        if self.cred is None:
            with open(self.credJsonFilePath, "r") as file:
                self.cred = json.load(file)

    def get_account_trade_history(self):
        self.get_cred()
        response = self.accountTradeHistory.get_account_trade_history(self.cred)
        return response

    def get_active_order_count(self, market):
        self.get_cred()
        response = self.activeOrderCountFactory.get_active_order_count(self.cred, market)
        return response

    def order_coin(self, side, market, price_per_unit, total_quantity):
        self.get_cred()
        response = self.sellCoinFactory.run_order(self.cred, side, market, price_per_unit, total_quantity)
        return response

    def check_order_status(self, order_id):
        self.get_cred()
        response = self.orderStatusFactory.check_order_status(self.cred, order_id)
        return response
