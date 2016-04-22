import sys

_is_win = sys.platform[:3].upper() == 'WIN'

if _is_win:
    DEBUG_FULL_NEWS_PATH = 'D:/temp/csf_news/'
    DEBUG_HOT_NEWS_PATH = 'D:/temp/csf_hot_news/'
else:
    DEBUG_FULL_NEWS_PATH = '/data/news/csf_news/'
    DEBUG_HOT_NEWS_PATH = '/data/news/csf_hot_news/'

DEBUG_MONGO_HOST = '192.168.250.208'
DEBUG_MONGO_PORT = 27017
DEBUG_MONGO_DB = 'news'
DEBUG_MONGO_TOP_TBALE = 'topnews_analyse'
DEBUG_MONGO_HOT_TBALE = 'hotnews_analyse'

DEBUG_TOP_MONGO_ARGS = (DEBUG_MONGO_HOST, DEBUG_MONGO_PORT, DEBUG_MONGO_DB, DEBUG_MONGO_TOP_TBALE)
DEBUG_HOT_MONGO_ARGS = (DEBUG_MONGO_HOST, DEBUG_MONGO_PORT, DEBUG_MONGO_DB, DEBUG_MONGO_HOT_TBALE)
