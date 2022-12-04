import json

coinListFile = "../excelModule/coinList.json"
with open(coinListFile, "r") as file:
    COIN_LIST = json.load(file)

# Control constants
FORCE_RUN = True
REPEAT_RUN_SLEEP_TIME = 20
FORCE_CHECK_AFTER_LOOP = 200

ERROR_SLEEP_TIME = 60
LAST_FILLED_ORDER_ADDRESS = "I2"
LAST_ORDER_STATUS_ADDRESS = "I3"

# Address row column
COIN_NAME_ADDRESS = "A1"
COIN_STATUS_ADDRESS = "A2"
OPEN_TRADE_COUNT_ADDRESS = "A4"

# current status
STATUS_COLUMN = 'M'

# Trade price and price
QUANTITY_COLUMN = 'N'
TO_BUY_COLUMN = 'O'
TO_SELL_COLUMN = 'P'

ID_BUY_COLUMN = 'V'
ID_SELL_COLUMN = 'W'
MESSAGE_COLUMN = 'Y'

# Excel file constants
EXCEL_RESOURCES = "../excelModule/resources"
BACKUP = "../excelModule/backup"

OPEN_TRADE_FILENAME = "excelOpenTradeData.xlsx"
EXECUTED_TRADE_FILENAME = "excelExecutedTradeData.xlsx"

OPEN_TRADE_FILE = EXCEL_RESOURCES + "/" + OPEN_TRADE_FILENAME
EXECUTED_TRADE_FILE = EXCEL_RESOURCES + "/" + EXECUTED_TRADE_FILENAME

# Open trade Excel sheet names
OPEN_TRADE_RULE_SHEET_NAME = "Control"

# string
ORDER_ID_STRING = "order_id"
MARKET_STRING = "market"
READY_STRING = "Ready"
COUNT_STRING = "count"
STATUS_STRING = "status"
