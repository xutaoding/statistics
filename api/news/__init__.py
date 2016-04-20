from statistics import StatisticsBefore
from statistics import StatisticsAfter

from eggs.utils import json_data


def get_topnews(query_date=None, rtype=False):
    """
    Parse to statistics data from hot news from news path or top news from mongo

    :param query_date: string, yyyymmdd format and length is 8
    :param rtype: int, if rtype is False, get data from news path, otherwose get data from mongo
    :return: json data format
    """
    if int(rtype) == 0:
        data = StatisticsBefore(query_date).topnews
    else:
        data = StatisticsAfter(query_date).topnews
    return json_data(data)


def get_hotnews(query_date=None, rtype=0):
    """
        Parse to statistics data from full news from news path or hot news from mongo

        :param query_date: string, yyyymmdd format and length is 8
        :param rtype: int, if rtype is False, get data from news path, otherwose get data from mongo
        :return: json data format
    """
    if int(rtype) == 0:
        data = StatisticsBefore(query_date).hotnews
    else:
        data = StatisticsAfter(query_date).hotnews
    return json_data(data)







