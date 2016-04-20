from django.http import HttpResponse
from django.shortcuts import render

from .. import BaseView
from api.news import get_hotnews, get_topnews


class NewsStatistic(BaseView):
    @staticmethod
    def get(request):
        rtype = request.GET.get('rtype')
        query = request.GET.get('query')
        print 'query:', query, request.GET
        json_data = get_topnews(query, rtype=rtype)
        return HttpResponse(content=json_data, content_type='application/json')

    def post(self, request):
        return HttpResponse('Hello world')

