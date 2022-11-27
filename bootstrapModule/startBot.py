from excelModule.excelTradeService import ExcelTradeService


class StartBot:
    excelTradeService = ExcelTradeService()

    def start(self):
        self.excelTradeService.start_job()
        return


startBot = StartBot()
startBot.start()
