import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Database.models import Anime1AnimateInfoModel
from Tools.anime1 import Anime1
from Tools.db import DB
from Tools.urls import Anime1AnimateUrl


class Anime1AnimateListView(APIView):
    @method_decorator(cache_page(300))
    def get(self, request):
        data = Anime1.get_home_animate_data()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class Anime1AnimateInfoView(APIView):
    def post(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response(status=status.HTTP_404_NOT_FOUND)
        animate_url = f'{Anime1AnimateUrl}{url}'
        data = DB.Cache.get_cache_data(key=animate_url)
        if request.data:
            model = DB.Anime1.create_animate_info(**request.data)
        else:
            model = DB.Anime1.get_animate_info(url=url)
        if not data:
            data = Anime1.get_animate_info(url=animate_url)
            DB.Cache.set_cache_data(key=animate_url, data=json.dumps(data), timeout=300)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
