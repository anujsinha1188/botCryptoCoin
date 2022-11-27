import os
import shutil

from _datetime import datetime
from excelModule.excelErrorService import ExcelErrorService
from excelModule.excelConst import BACKUP, OPEN_TRADE_FILENAME, EXECUTED_TRADE_FILENAME, OPEN_TRADE_FILE, \
    EXECUTED_TRADE_FILE


class ExcelBackupService:
    excelErrorService = ExcelErrorService()

    def create_backup(self):

        backup_trade_file = BACKUP + "/" + OPEN_TRADE_FILENAME
        backup_trade_file_in_time = BACKUP + "/" + datetime.now().strftime("%Y-%b-%d_%H") + "_" + OPEN_TRADE_FILENAME
        backup_executed_trade_file = BACKUP + "/" + EXECUTED_TRADE_FILENAME
        backup_executed_trade_file_in_time = \
            BACKUP + "/" + datetime.now().strftime("%Y-%b-%d_%H") + "_" + EXECUTED_TRADE_FILENAME

        try:
            shutil.copy2(OPEN_TRADE_FILE, backup_trade_file)
            os.replace(backup_trade_file, backup_trade_file_in_time)

            shutil.copy2(EXECUTED_TRADE_FILE, backup_executed_trade_file)
            os.replace(backup_executed_trade_file, backup_executed_trade_file_in_time)

        except Exception as error:
            self.excelErrorService.handel_error(error)
