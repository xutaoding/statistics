from django.conf.urls import url

from views import NewsStatistic

urlpatterns = [
    url(r'api/data.json$', NewsStatistic.as_view(), name='statistic'),
]
