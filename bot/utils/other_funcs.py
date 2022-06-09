# Очистка имени пользователя от тэгов
import datetime
from dateutil import tz


def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "*")
    if ">" in firstname: firstname = firstname.replace(">", "*")
    return firstname

# Получение текущей даты
def get_dates():
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Ukraine/Kiev')
    utc = datetime.datetime.utcnow().replace(microsecond=0)
    utc = utc.replace(tzinfo=from_zone)
    now_time = utc.astimezone(to_zone)
    now_time = str(now_time).split("+")[0]
    return now_time