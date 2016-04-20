import simplejson


def json_data(obj, depth=1, ignore=None):
    ignore = ignore or []
    required_keys = list(set(obj) - set(ignore))
    news_obj = {key: obj[key] for key in required_keys}
    return simplejson.dumps(news_obj)


