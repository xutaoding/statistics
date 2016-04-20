import os
import re
import linecache
from os.path import join
from datetime import date
from collections import defaultdict

from tld import get_tld
from eggs.conf import news
from eggs.dbs import Mongodb


class Config(object):
    def __init__(self, query_date):
        self.query_date = query_date

    @property
    def hot_news_path(self):
        return news.HOT_NEWS_PATH + self.query_date + '/'

    @property
    def full_news_path(self):
        return news.FULL_NEWS_PATH + self.query_date + '/'

    @property
    def top_mongo_args(self):
        return news.TOP_MONGO_ARGS

    @property
    def hot_mongo_args(self):
        return news.HOT_MONGO_ARGS


class StatisticsBase(Config):
    def __init__(self, query_date=None):
        if query_date is None:
            self.query_date = str(date.today()).replace('-', '')
        else:
            if not isinstance(query_date, basestring) or len(query_date) != 8:
                raise ValueError("<query_date> must string and length is 8")
            self.query_date = query_date

        super(StatisticsBase, self).__init__(self.query_date)

        self.topnews = self._parse(self._hot_dataset())
        self.hotnews = self._parse(self._top_dataset())

    def _top_dataset(self):
        raise NotImplemented

    def _hot_dataset(self):
        raise NotImplemented

    @staticmethod
    def _parse(dataset):
        dt_dist = 'dt_dist'
        result = defaultdict(lambda: defaultdict(int))

        for uri, cat, dt in dataset:
            domain = get_tld(uri, as_object=True).domain
            result[domain][cat] += 1
            result[domain]['count'] += 1

            if dt_dist not in result[domain]:
                result[domain][dt_dist] = [dt]
            else:
                result[domain][dt_dist].append(dt)

        for site_domain in result:
            result[site_domain][dt_dist].sort()
        return result

    def show(self):
        def inner(dataset):
            for site, vaules in dataset.iteritems():
                print('News show:')
                for _key, _count in vaules.iteritems():
                    print('\t{}->{}: {}'.format(site, _key, _count))

        inner(self.topnews)
        print('top site len: {}'.format(len(self.topnews)))
        inner(self.hotnews)
        print('all site len: {}'.format(len(self.hotnews)))


class StatisticsBefore(StatisticsBase):
    @staticmethod
    def _get_data_from_files(path):
        data = []
        today = str(date.today()).replace('-', '')

        for root, dirs, files in os.walk(path):
            for filename in files:
                abs_filename = join(root, filename)
                url = linecache.getline(abs_filename, 1).strip()
                dt = linecache.getline(abs_filename, 2).strip()
                cat = linecache.getline(abs_filename, 4).strip()

                if dt.startswith(today):
                    data.append((url, cat, dt))
        return data

    def _top_dataset(self):
        hot_path = self.hot_news_path
        return self._get_data_from_files(hot_path)

    def _hot_dataset(self):
        full_path = self.full_news_path
        return self._get_data_from_files(full_path)


class StatisticsAfter(StatisticsBase):
    def _get_data_from_mongo(self, *mongo_args):
        mongo = Mongodb(*mongo_args)
        fields = {'url': 1, 'cat': 1, 'dt': 1}
        query = {'dt': re.compile(r'%s' % self.query_date)}

        return [(docs['url'], docs['cat'], docs['dt']) for docs in mongo.query(query, fields)]

    def _top_dataset(self):
        return self._get_data_from_mongo(*self.top_mongo_args)

    def _hot_dataset(self):
        return self._get_data_from_mongo(*self.hot_mongo_args)

