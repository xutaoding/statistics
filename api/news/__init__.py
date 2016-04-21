import simplejson
from statistics import StatisticsBefore
from statistics import StatisticsAfter


def get_topnews(query_start=None, query_end=None, rtype=False):
    """
    Parse to statistics data from hot news from news path or top news from mongo

    :param query_start: string, yyyymmdd format and length is 8, query data start date
    :param query_end: string, yyyymmdd format and length is 8, query data end date
    :param rtype: int, if rtype is False, get data from news path, otherwose get data from mongo
    :return: json data format
    """
    query_args = (query_start, query_end)
    if int(rtype) == 0:
        data = StatisticsBefore(*query_args).topnews_dataset
    else:
        data = StatisticsAfter(*query_args).hotnews_dataset
    return simplejson.dumps(data)


def get_hotnews(query_start=None, query_end=None, rtype=0):
    """
        Parse to statistics data from full news from news path or hot news from mongo

        :param query_start: string, yyyymmdd format and length is 8, query data start date
        :param query_end: string, yyyymmdd format and length is 8, query data end date
        :param rtype: int, if rtype is False, get data from news path, otherwose get data from mongo
        :return: json data format
    """
    query_args = (query_start, query_end)
    if int(rtype) == 0:
        data = StatisticsBefore(*query_args).hotnews_dataset
    else:
        data = StatisticsAfter(*query_args).hotnews_dataset
    return simplejson.dumps(data)


def get_total_dataset(query_start=None, query_end=None, rtype=0):
    """
    Parse to statistics data from all specified news path or all specified query condition mongo data

    :param query_start: string, yyyymmdd format and length is 8, query data start date
    :param query_end: string, yyyymmdd format and length is 8, query data end date
    :param rtype: int, if rtype is False, get data from news path, otherwose get data from mongo
    :return:
    """
    query_args = (query_start, query_end)
    if int(rtype) == 0:
        data = StatisticsBefore(*query_args).total_dataset
    else:
        data = StatisticsAfter(*query_args).total_dataset
    return simplejson.dumps(data)







