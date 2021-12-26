import json

from django.core.cache import caches
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from Database.models import AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from django.views import View

from Api.serializers.anime1 import Anime1InfoSerializer
from Tools.anime1 import Anime1
from Tools.db import DB
from Tools.urls import Anime1AnimateUrl


class TestView(APIView):
    def get(self, request):
        cache_db = caches['default']
        cache_db.clear()
        # for i in cache_db.keys('*'):
        #     print(i)
        #     print(cache_db.get(key).data)
        return Response({}, status=status.HTTP_200_OK)
