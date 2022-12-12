import datetime
import time


def datetime_to_unix(n: datetime.datetime) -> int:
    return int(time.mktime(n.timetuple()))
