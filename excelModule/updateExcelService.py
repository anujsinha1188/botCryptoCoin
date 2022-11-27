from utilityModule.utilityModule import get_date_time
from excelModule.excelConst import STATUS_COLUMN, MESSAGE_COLUMN, OPEN_TRADE_FILE, ID_BUY_COLUMN, ID_SELL_COLUMN


class UpdateExcelService:
    def update_error_status(self, response, open_trade_sheet, open_trade_row):
        print("Error response data: " + str(response))
        print("Error response message: " + response.get("message"))
        open_trade_sheet[STATUS_COLUMN + str(open_trade_row)].value = response.get("status")
        open_trade_sheet[MESSAGE_COLUMN + str(open_trade_row)].value = response.get("message")


    def update_buy_coin(self, response, open_trade_sheet, open_trade_row):
        print("Info: Update buy coin: " + str(response))
        open_trade_sheet[STATUS_COLUMN + str(open_trade_row)].value = "Check Buy"
        open_trade_sheet[ID_BUY_COLUMN + str(open_trade_row)].value = response.get("orders")[0].get("id")
        open_trade_sheet[MESSAGE_COLUMN + str(open_trade_row)].value = \
            get_date_time(response.get("orders")[0].get("created_at"))

    def update_buy_order(self, response, open_trade_sheet, open_trade_row):
        print("Info: Filled buy order: " + str(response))
        open_trade_sheet[STATUS_COLUMN + str(open_trade_row)].value = "Sell"
        open_trade_sheet['B' + str(open_trade_row)].value = get_date_time(response.get("updated_at"))
        open_trade_sheet['C' + str(open_trade_row)].value = response.get("market")
        open_trade_sheet['D' + str(open_trade_row)].value = response.get("side")
        open_trade_sheet['E' + str(open_trade_row)].value = response.get("avg_price")
        open_trade_sheet['F' + str(open_trade_row)].value = response.get("total_quantity")
        open_trade_sheet['G' + str(open_trade_row)].value = "=E" + str(open_trade_row) + "*F" + str(
            open_trade_row)
        open_trade_sheet['H' + str(open_trade_row)].value = response.get("fee_amount")
        open_trade_sheet['I' + str(open_trade_row)].value = "=G" + str(open_trade_row) + "+H" + str(
            open_trade_row)
        if open_trade_sheet["A3"].value == "No TDS":
            open_trade_sheet['J' + str(open_trade_row)].value = 0
        else:
            open_trade_sheet['J' + str(open_trade_row)].value = "=.01*(I" + str(open_trade_row) + "-H" + str(
                open_trade_row) + ")"
        open_trade_sheet['K' + str(open_trade_row)].value = "=I" + str(open_trade_row) + "+J" + str(
            open_trade_row)

    def update_sell_coin(self, response, open_trade_sheet, open_trade_row):
        print("Info: Update sell coin: " + str(response))
        open_trade_sheet[STATUS_COLUMN + str(open_trade_row)].value = "Check Sell"
        open_trade_sheet[ID_SELL_COLUMN + str(open_trade_row)].value = response.get("orders")[0].get("id")
        open_trade_sheet[MESSAGE_COLUMN + str(open_trade_row)].value = \
            get_date_time(response.get("orders")[0].get("created_at"))

    def update_sell_order(self, response, open_trade_sheet, open_trade_row, executed_trade_sheet):
        print("Info: Filled sell order: " + str(response))
        open_trade_sheet[STATUS_COLUMN + str(open_trade_row)].value = "Buy"
        self.fill_executed_trade(response, open_trade_sheet, open_trade_row, executed_trade_sheet)
        self.clear_open_trade(open_trade_sheet, open_trade_row)

    def fill_executed_trade(self, response, open_trade_sheet, open_trade_row, executed_trade_sheet):
        executed_trade_sheet["B6"] = open_trade_sheet['B' + str(open_trade_row)].value
        executed_trade_sheet["C6"] = open_trade_sheet['C' + str(open_trade_row)].value
        executed_trade_sheet["D6"] = open_trade_sheet['D' + str(open_trade_row)].value
        executed_trade_sheet["E6"] = open_trade_sheet['E' + str(open_trade_row)].value
        executed_trade_sheet["F6"] = open_trade_sheet['F' + str(open_trade_row)].value
        executed_trade_sheet["G6"] = "=E6*F6"
        executed_trade_sheet["H6"] = open_trade_sheet['H' + str(open_trade_row)].value
        executed_trade_sheet["I6"] = "=G6+H6"
        executed_trade_sheet["J6"] = open_trade_sheet['J' + str(open_trade_row)].value
        executed_trade_sheet["K6"] = "=I6+J6"

        executed_trade_sheet["L6"] = get_date_time(response.get("updated_at"))
        executed_trade_sheet["M6"] = response.get("market")
        executed_trade_sheet["N6"] = response.get("side")
        executed_trade_sheet["O6"] = response.get("avg_price")
        executed_trade_sheet["P6"] = response.get("total_quantity")
        executed_trade_sheet["Q6"] = "=O6*P6"
        executed_trade_sheet["R6"] = response.get("fee_amount")
        executed_trade_sheet["S6"] = "=Q6+R6"
        executed_trade_sheet["T6"] = "=Q6-R6-I6"
        executed_trade_sheet["U6"] = "=.01*(Q6-R6)"
        executed_trade_sheet["V6"] = "=T6-U6"
        executed_trade_sheet["W6"] = "=(T6/I6)*100"
        executed_trade_sheet["X6"] = ""

        executed_trade_sheet["Z6"] = open_trade_sheet[ID_BUY_COLUMN + str(open_trade_row)].value
        executed_trade_sheet["AA6"] = open_trade_sheet[ID_SELL_COLUMN + str(open_trade_row)].value

    def clear_open_trade(self, open_trade_sheet, open_trade_row):
        open_trade_sheet['B' + str(open_trade_row)].value = None
        open_trade_sheet['C' + str(open_trade_row)].value = None
        open_trade_sheet['D' + str(open_trade_row)].value = None
        open_trade_sheet['E' + str(open_trade_row)].value = None
        open_trade_sheet['F' + str(open_trade_row)].value = None
        open_trade_sheet['G' + str(open_trade_row)].value = None
        open_trade_sheet['H' + str(open_trade_row)].value = None
        open_trade_sheet['I' + str(open_trade_row)].value = None
        open_trade_sheet['J' + str(open_trade_row)].value = None
        open_trade_sheet['K' + str(open_trade_row)].value = None

        open_trade_sheet[ID_BUY_COLUMN + str(open_trade_row)].value = None
        open_trade_sheet[ID_SELL_COLUMN + str(open_trade_row)].value = None
        open_trade_sheet[MESSAGE_COLUMN + str(open_trade_row)] = None
