import datetime


def today():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
