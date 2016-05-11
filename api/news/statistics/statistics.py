# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import linecache
from datetime import date
from os.path import join, basename
from collections import defaultdict

from tld import get_tld
from eggs.conf import news
from eggs.dbs import Mongodb
from eggs.utils import FailureMsg, get_date_range


class Config(object):
    category = {
        'hot': '热点新闻',
        'hjd': '热点新闻',
        'us_gg': '美股个股',
        'us_hg': '美股宏观',
        'us_gs': '美股股市',
        'us_hy': '美股行业',
    }

    def __init__(self, query_start, query_end):
        self.query_start = query_start
        self.query_end = query_end

    @property
    def hot_news_path_range(self):
        return [news.HOT_NEWS_PATH + _date + '/' for _date in get_date_range(self.query_start, self.query_end)]

    @property
    def full_news_path_range(self):
        return [news.FULL_NEWS_PATH + _date + '/' for _date in get_date_range(self.query_start, self.query_end)]

    @property
    def top_mongo_args(self):
        return news.TOP_MONGO_ARGS

    @property
    def hot_mongo_args(self):
        return news.HOT_MONGO_ARGS


class StatisticsBase(Config, FailureMsg):
    def __init__(self, query_start=None, query_end=None):
        today = str(date.today()).replace('-', '')
        super(StatisticsBase, self).__init__(
            query_start=query_start or today,
            query_end=query_end or today
        )

    @property
    def topnews_dataset(self):
        valid, error_msg = self.validity
        if not valid:
            return error_msg
        return self._parse(self._top_dataset())

    @property
    def hotnews_dataset(self):
        valid, error_msg = self.validity
        if not valid:
            return error_msg
        return self._parse(self._hot_dataset())

    @property
    def total_dataset(self):
        valid, error_msg = self.validity
        if not valid:
            return error_msg
        return self._parse(self._total_dataset())

    def _top_dataset(self):
        raise NotImplementedError

    def _hot_dataset(self):
        raise NotImplementedError

    def _total_dataset(self):
        raise NotImplementedError

    @property
    def validity(self):
        """ Validate arguments whether correct or not """
        info = '<query_start>: {}, <query_end>: {}'.format(self.query_start, self.query_end)

        if (not isinstance(self.query_start, basestring) or len(self.query_start)) != 8 or \
                (not isinstance(self.query_end, basestring) or len(self.query_end)) != 8:
            return False, self.get_error_msg(error_type=105, info=info)
        elif self.query_start > self.query_end:
            return False, self.get_error_msg(error_type=205, info=info)
        return True, self.get_error_msg()

    def convert_cat(self, cat):
        return self.category.get(cat, cat)

    def _parse(self, dataset):
        """
        Parse data to calculate and sort about news
        :param dataset: list, list of dict that query date as key, value is tuple, including url, cat and pub_date on news
        :return: sorted dataset, type like as: [{'20160420': {...}}, ...]
        """
        total_data = []
        dt_dist = 'dt_dist'  # Key to news publish datetime distribute

        for dict_to_date in dataset:
            for query_date, data_list in dict_to_date.iteritems():
                # `query_date` is date string, `data_list` is list
                result = defaultdict(lambda: defaultdict(int))
                for uri, cat, dt in data_list:
                    try:
                        domain = get_tld(uri, as_object=True).domain
                        result[domain][cat] += 1
                        result[domain]['count'] += 1
                        result[domain].setdefault(dt_dist, []).append(dt)
                    except Exception:
                        pass

                for site_domain in result.keys():
                    result[site_domain][dt_dist].sort()
                    result['total_count'] = result.get('total_count', 0) + len(result[site_domain][dt_dist])
                total_data.append({query_date: result})
        return total_data


class StatisticsBefore(StatisticsBase):
    """
    Statistics crawled news before analysis
    """
    def _get_data_from_files(self, date_path_range):
        """
        retrieval all data from crawled news files
        :param date_path_range: list, a list of path base on date, eg: ['/.../20160419/', '/.../20160420/', ...]
        :return: list, a list of dict that query_date as key,
            value including news url, news category and news publish datetime
        """
        data = []

        for date_path in date_path_range:
            current_date = basename(date_path[:-1])
            data_from_date = {current_date: []}

            for root, dirs, files in os.walk(date_path):
                for filename in files:
                    abs_filename = join(root, filename)
                    url = linecache.getline(abs_filename, 1).strip()
                    dt = linecache.getline(abs_filename, 2).strip()
                    cat = linecache.getline(abs_filename, 4).strip()

                    if dt.startswith(current_date):
                        data_from_date[current_date].append((url, self.convert_cat(cat), dt))
            data.append(data_from_date)
        return data

    def _top_dataset(self):
        return self._get_data_from_files(self.hot_news_path_range)

    def _hot_dataset(self):
        return self._get_data_from_files(self.full_news_path_range)

    def _total_dataset(self):
        dataset = self._hot_dataset()
        pos = (lambda k: [i for i, d in enumerate(dataset) if k in d])

        for each_dict in self._top_dataset():
            for query_day, dt_list in each_dict.iteritems():
                index = pos(query_day)
                if index:
                    dataset[index[0]].setdefault(query_day, []).extend(dt_list)
        return dataset


class StatisticsAfter(StatisticsBase):
    """
        After statistical analysis of the news
    """

    def _get_data_from_mongo(self, *mongo_args):
        """
        Obtain all dataset from mongo base on query condition
        :param mongo_args: tuple, (host, port db, table)
        :return: list, a list of dict that query_date as key,
            value including news url, news category and news publish datetime
        """
        result = defaultdict(list)
        mongo = Mongodb(*mongo_args)
        fields = {'url': 1, 'cat': 1, 'dt': 1}
        date_range = get_date_range(self.query_start, self.query_end)
        date_range.sort()
        query = {'dt': {
            '$gte': date_range[0] + '000000',
            '$lte': date_range[-1] + '235959'
        }}

        for docs in mongo.query(query, fields):
            dt = docs['dt']
            result[dt[:8]].append((docs['url'], self.convert_cat(docs['cat']), dt))
        return [{k: v} for k, v in result.iteritems()]

    def _top_dataset(self):
        return self._get_data_from_mongo(*self.top_mongo_args)

    def _hot_dataset(self):
        return self._get_data_from_mongo(*self.hot_mongo_args)

    def _total_dataset(self):
        return self._hot_dataset()

