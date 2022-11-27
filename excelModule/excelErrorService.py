import time

from excelModule.excelConst import ERROR_SLEEP_TIME
from utilityModule.utilityModule import get_date_time


class ExcelErrorService:
    def handel_error(self, error):
        print(str(error))
        print("Error Time: " + get_date_time(time.time()))
        print("Info: sleep for " + str(ERROR_SLEEP_TIME) + " seconds.")
        time.sleep(ERROR_SLEEP_TIME)
        print("Info: Resume")
        time.sleep(1)
