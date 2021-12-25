import json

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
        # url = request.query_params.get('url')
        # if not url:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        animate_url = f'{Anime1AnimateUrl}/?cat=952'
        # data = DB.Cache.get_cache_data(key=animate_url)
        # if data:
        #     return Response(data, status=status.HTTP_200_OK)
        # _ = {'name': '古見同學有交流障礙症。', 'url': '/?cat=952', 'episode': '1-12', 'years': '2021', 'season': '秋', 'subtitle_group': '幻櫻'}
        # if request.data:
        #     model = DB.Anime1.create_animate_info(**request.data)
        # else:
        model = DB.Anime1.get_animate_info(url='/?cat=952')
        episode_data = Anime1.get_animate_info(url=animate_url)
        DB.Anime1.update_or_create_many_episode(episodes=episode_data, owner=model)
        # DB.Cache.set_cache_data(key=animate_url, data=json.dumps(episode_data), timeout=300)
        serializer = Anime1InfoSerializer(model)
        return Response({}, status=status.HTTP_200_OK)
