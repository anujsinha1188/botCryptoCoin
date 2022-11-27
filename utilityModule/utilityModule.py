from _datetime import datetime


def get_date_time(timestamp):
    date_time = datetime.fromtimestamp(timestamp / 1000)
    return date_time.strftime("%d-%b-%y, %H:%M:%S")


def get_current_month():
    return datetime.now().strftime("%b")