from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Api.serializers import Anime1AnimateEpisodeInfoSerializer, Anime1AnimateInfoSerializer
from Api.views.base import BaseAnimateEpisodeDone
from Database.models import Anime1AnimateEpisodeInfoModel, Anime1AnimateInfoModel
from Tools.anime1 import Anime1
from Tools.db import DB, MyPageNumberPagination
from Tools.urls import Anime1AnimateUrl, Anime1AnimatePWUrl


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
        if not request.query_params.get('url'):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'cat=' in request.query_params.get('url'):
            animate_url = f'{Anime1AnimatePWUrl}/?cat={request.query_params.get("url").split("=")[1]}'
        else:
            animate_url = f'{Anime1AnimateUrl}/?cat={url}'
        data = DB.Cache.get_cache_data(animate_url)
        if data:
            model = DB.Anime1.get_animate_info(name=data['animate_name'])
        else:
            animate_data = Anime1.get_animate_info(url=animate_url, data=[])
            model = DB.Anime1.update_or_create_animate_info(url=url, name=animate_data['animate_name'])
            DB.Anime1.update_or_create_many_episode(episodes=animate_data['episode_data'], owner=model)
            DB.Cache.set_cache_data(key=animate_url, data=animate_data, timeout=1800)
        serializer = Anime1AnimateInfoSerializer(model)
        return Response(serializer.data)


class Anime1AnimateInfoEpisodeView(ListAPIView):
    serializer_class = Anime1AnimateEpisodeInfoSerializer
    queryset = Anime1AnimateEpisodeInfoModel.objects.select_related('owner').all()

    def list(self, request, *args, **kwargs):
        model = Anime1AnimateEpisodeInfoModel.objects.filter(owner_id=kwargs.get('animate_id'))
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Anime1AnimateEpisodeInfoSerializer(model, many=True)
        return Response(serializer.data)


class Anime1AnimateEpisodeDoneView(BaseAnimateEpisodeDone, ListAPIView):
    serializer_class = Anime1AnimateInfoSerializer
    queryset = Anime1AnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination
    animate_info_model = Anime1AnimateInfoModel
    animate_episode_info_model = Anime1AnimateEpisodeInfoModel


class Anime1MenuSeasonView(APIView):
    @method_decorator(cache_page(300))
    def get(self, request):
        data = Anime1.get_home_season_url()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class Anime1SeasonView(APIView):
    @method_decorator(cache_page(300))
    def get(self, request, season):
        data = Anime1.get_season_list(season=season)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class Anime1DestroyManyAnimate(APIView):
    def delete(self, request):
        delete_list = request.data.get('deleteArray')
        DB.Anime1.delete_animate_episode(id__in=delete_list)
        DB.My.create_log(msg='Anime1 刪除已選取動漫', action='delete')
        return Response(status=status.HTTP_204_NO_CONTENT)
