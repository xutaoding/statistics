from django.http import HttpResponse
from django.shortcuts import render

from .. import BaseView
from api.news import get_total_dataset


class NewsStatistic(BaseView):
    @staticmethod
    def get(request):
        rtype = request.GET.get('rtype')
        query_end = request.GET.get('end')
        query_start = request.GET.get('start')
        json_data = get_total_dataset(query_start, query_end, rtype=rtype)
        return HttpResponse(content=json_data, content_type='application/json')

    @staticmethod
    def post(request):
        pass

