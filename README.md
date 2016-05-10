1：对新闻各站点的统计分析：
------------------------
URL: http://54.223.52.50:7900/news/api/data.json

查询字符串参数：

start：查询起始日期，格式：yyyymmdd， 长度为8

end：查询结束日期，格式：yyyymmdd， 长度为8

rtype：查询数据来源：1 为分析后从Mongo数据库查询， 0为新闻抓取后分析前查询

响应格式：json

示例：
-----
http://54.223.52.50:7900/news/api/data.json?start=20160420&end=20160421&rtype=1

start:
------
(54.223.52.50)
/opt/interface/uwsgi/src/uwsgi-2.0.12/uwsgi --http :7900 --chdir /opt/interface/statistics --module statistics.django_uwsgi --pythonpath /opt/venv2.7.10/lib64/python2.7/site-packages
