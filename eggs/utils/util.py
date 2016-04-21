import six
from datetime import date, timedelta


def get_date_range(start, end):
    """
    calculate date range
    :param start: string, yyyymmdd, start date
    :param end: string, yyyymmdd, end date
    :return: list, date range list
    """
    date_range = []
    split_ymd = (lambda _d: (int(_d[:4]), int(_d[4:6]), int(_d[6:8])))
    date_start = date(*split_ymd(start))
    date_end = date(*split_ymd(end))

    while date_start <= date_end:
        date_range.append(str(date_start).replace('-', ''))
        date_start = timedelta(days=1) + date_start
    return date_range


def depth(d):
    """
    Calculate the depth of the dictionary
    :param d: dict, dictionary, maybe have sub dictionary
    :return: int, dictionary depth
    """
    dpth = 1
    dicts = [v for k, v in six.iteritems(d) if isinstance(v, dict)]

    if not dicts:
        return dpth
    return dpth + max([depth(obj) for obj in dicts])

