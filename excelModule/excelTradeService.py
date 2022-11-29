import sys
import time
import openpyxl

from excelModule.excelConst import ORDER_ID_STRING, OPEN_TRADE_FILE, EXECUTED_TRADE_FILE, OPEN_TRADE_RULE_SHEET_NAME, \
    LAST_FILLED_ORDER_ADDRESS, REPEAT_RUN_SLEEP_TIME, COIN_LIST, MARKET_STRING, COIN_NAME_ADDRESS, \
    COIN_STATUS_ADDRESS, READY_STRING, OPEN_TRADE_COUNT_ADDRESS, COUNT_STRING, STATUS_COLUMN, TO_BUY_COLUMN, \
    TO_SELL_COLUMN, QUANTITY_COLUMN, ID_BUY_COLUMN, ID_SELL_COLUMN, STATUS_STRING, FORCE_CHECK_AFTER_LOOP
from excelModule.excelErrorService import ExcelErrorService
from excelModule.updateExcelService import UpdateExcelService
from excelModule.excelBackupService import ExcelBackupService
from coinModule.coinService import CoinService
from utilityModule.utilityModule import get_current_month


class ExcelTradeService:

    excelErrorService = ExcelErrorService()
    updateExcelService = UpdateExcelService()
    excelBackupService = ExcelBackupService()

    coinService = CoinService()

    forceRun = True
    repeatRunSleepTime = REPEAT_RUN_SLEEP_TIME
    orderExecuted = False
    checkOrderCount = 0

    openTradeWorkbook = None
    executedTradeWorkbook = None

    openTradeSheet = None
    executedTradeSheet = None

    openTradeRow = None

    coin_tradeCode = None

    def get_workbook(self):
        if self.openTradeWorkbook is None:
            self.openTradeWorkbook = openpyxl.load_workbook(OPEN_TRADE_FILE)
        if self.executedTradeWorkbook is None:
            self.executedTradeWorkbook = openpyxl.load_workbook(EXECUTED_TRADE_FILE)

    def get_rule_sheet(self):
        try:
            self.openTradeSheet = self.openTradeWorkbook[OPEN_TRADE_RULE_SHEET_NAME]
        except KeyError as error:
            self.excelErrorService.handel_error(error)
            sys.exit()

    def is_open_order_executed(self):
        try:
            order_executed = False
            response_trade_history = self.coinService.get_account_trade_history()
            trade_id = response_trade_history[0].get(ORDER_ID_STRING)
            response_order_status = self.coinService.check_order_status(trade_id)
            if response_order_status.get("status") == "filled":
                if trade_id != self.openTradeSheet[LAST_FILLED_ORDER_ADDRESS].value:
                    order_executed = True
                    self.openTradeSheet[LAST_FILLED_ORDER_ADDRESS].value = trade_id
                self.repeatRunSleepTime = REPEAT_RUN_SLEEP_TIME
            else:
                self.repeatRunSleepTime = REPEAT_RUN_SLEEP_TIME * 4
                self.forceRun = True

            return order_executed
        except Exception as error:
            self.excelErrorService.handel_error(error)

    def start_job(self):
        resume_check = True
        self.get_workbook()
        self.get_rule_sheet()

        while resume_check:
            self.checkOrderCount += 1
            if self.checkOrderCount > FORCE_CHECK_AFTER_LOOP:
                self.forceRun = True
                self.checkOrderCount = 0
            if self.forceRun or self.is_open_order_executed():
                self.run_job()
            else:
                print("No open trade executed.")

            print("Info: Sleep for " + str(self.repeatRunSleepTime) + " seconds.")
            time.sleep(self.repeatRunSleepTime)
            print("Resume.")
            time.sleep(1)

    def run_job(self):
        self.orderExecuted = False
        for coin in COIN_LIST:
            self.coin_tradeCode = coin.get(MARKET_STRING)

            try:
                self.openTradeSheet = self.openTradeWorkbook[self.coin_tradeCode]

                response_order_count = self.coinService.get_active_order_count(self.coin_tradeCode)
                count = response_order_count.get(COUNT_STRING)
                if self.forceRun:
                    print("Force running for: " + self.coin_tradeCode)
                    self.openTradeSheet[OPEN_TRADE_COUNT_ADDRESS].value = count
                    self.process_coin()
                else:
                    if self.openTradeSheet[COIN_NAME_ADDRESS].value == self.coin_tradeCode \
                            and self.openTradeSheet[COIN_STATUS_ADDRESS].value == READY_STRING:
                        if count != self.openTradeSheet[OPEN_TRADE_COUNT_ADDRESS].value:
                            print("Running: " + self.coin_tradeCode + ". Trade count: " + str(count))
                            self.openTradeSheet[OPEN_TRADE_COUNT_ADDRESS].value = count
                            self.openTradeWorkbook.save(OPEN_TRADE_FILE)
                            self.process_coin()
                        else:
                            print("No change in trade count: " + self.coin_tradeCode +
                                  ". Trade count: " + str(count) + ".")

            except Exception as error:
                self.excelErrorService.handel_error(error)

        if self.orderExecuted:
            self.repeatRunSleepTime = 1
            self.checkOrderCount = 0
            self.forceRun = True
        else:
            self.forceRun = False

    def process_coin(self):
        self.openTradeRow = 4
        end_of_file = False
        while not end_of_file:
            if self.openTradeRow == 1000:
                print("Error: In XLService class process_coin function, Error in while loop")
                sys.exit()
            self.openTradeRow += 1
            status = self.openTradeSheet[STATUS_COLUMN + str(self.openTradeRow)].value
            if status == "Ignore":
                continue
            elif status == "Buy":
                self.order_coin("buy")
            elif status == "Sell":
                self.order_coin("sell")
            elif status == "Check Buy":
                self.check_order_status("buy")
            elif status == "Check Sell":
                self.check_order_status("sell")
            elif status == "End":
                end_of_file = True

    def order_coin(self, side):
        self.orderExecuted = True
        market = self.coin_tradeCode
        price_per_unit = None
        response = None

        if side == "buy":
            price_per_unit = self.openTradeSheet[TO_BUY_COLUMN + str(self.openTradeRow)].value
        elif side == "sell":
            price_per_unit = self.openTradeSheet[TO_SELL_COLUMN + str(self.openTradeRow)].value

        total_quantity = self.openTradeSheet[QUANTITY_COLUMN + str(self.openTradeRow)].value
        try:
            response = self.coinService.order_coin(side, market, price_per_unit, total_quantity)
            if side == "buy":
                self.updateExcelService. \
                    update_buy_coin(response, self.openTradeSheet, self.openTradeRow)
            elif side == "sell":
                self.updateExcelService. \
                    update_sell_coin(response, self.openTradeSheet, self.openTradeRow)
            self.openTradeWorkbook.save(OPEN_TRADE_FILE)
        except Exception as error:
            if response is not None and response.get(STATUS_STRING) == "error":
                print(str(error))
                self.updateExcelService. \
                    update_error_status(response, self.openTradeSheet, self.openTradeRow)
                self.openTradeWorkbook.save(OPEN_TRADE_FILE)
            else:
                self.excelErrorService.handel_error(error)

    def check_order_status(self, side):
        order_id = None

        if side == "buy":
            order_id = self.openTradeSheet[ID_BUY_COLUMN + str(self.openTradeRow)].value
        elif side == "sell":
            order_id = self.openTradeSheet[ID_SELL_COLUMN + str(self.openTradeRow)].value

        try:
            response = self.coinService.check_order_status(order_id)
            if response.get('status') == "error":
                self.updateExcelService. \
                    update_error_status(response, self.openTradeSheet, self.openTradeRow)
                self.openTradeWorkbook.save(OPEN_TRADE_FILE)
            elif response.get("status") == "filled":
                if side == "buy":
                    self.updateExcelService.update_buy_order(response, self.openTradeSheet, self.openTradeRow)
                    self.openTradeWorkbook.save(OPEN_TRADE_FILE)
                    self.order_coin("sell")
                elif side == "sell":
                    self.assign_executed_trade_sheet(response)
                    self.executedTradeSheet.insert_rows(6)
                    self.executedTradeWorkbook.save(EXECUTED_TRADE_FILE)
                    self.updateExcelService.update_sell_order(
                        response, self.openTradeSheet, self.openTradeRow, self.executedTradeSheet)
                    self.openTradeWorkbook.save(OPEN_TRADE_FILE)
                    self.executedTradeWorkbook.save(EXECUTED_TRADE_FILE)
                    self.order_coin("buy")
                self.excelBackupService.create_backup()
        except Exception as error:
            self.excelErrorService.handel_error(error)

    def assign_executed_trade_sheet(self, response):
        if response.get("market").endswith("INR"):
            self.executedTradeSheet = self.executedTradeWorkbook[get_current_month()]
        else:
            self.executedTradeSheet = self.executedTradeWorkbook[get_current_month() + "USDT"]
