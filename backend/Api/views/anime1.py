from django.db.models import Model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Api.serializers import Anime1AnimateEpisodeInfoSerializer, Anime1AnimateInfoSerializer
from Api.views.base import BaseAnimateEpisodeDone
from Database.models import Anime1AnimateEpisodeInfoModel, Anime1AnimateInfoModel
from Tools.anime1 import Anime1
from Tools.db import DB, MyPageNumberPagination
from Tools.swagger import Anime1AnimateSwagger, Anime1AnimateInfoSwagger, Anime1AnimateInfoEpisodeSwagger, \
    Anime1AnimateEpisodeDoneSwagger, Anime1MenuSeasonSwagger, Anime1DestroyManyAnimateSwagger, Anime1SeasonSwagger
from Tools.urls import Anime1AnimateUrl, Anime1AnimatePWUrl


@method_decorator(**Anime1AnimateSwagger.rs)
class Anime1AnimateListView(ModelViewSet):
    my_tags = ['Anime1首頁動漫資料']

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        data = Anime1.get_home_animate_data()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(**Anime1AnimateInfoSwagger.c)
class Anime1AnimateInfoView(ModelViewSet):
    my_tags = ['Anime1動漫資料']

    def create(self, request, *args, **kwargs):
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


@method_decorator(**Anime1AnimateInfoEpisodeSwagger.rs)
class Anime1AnimateInfoEpisodeView(ModelViewSet):
    serializer_class = Anime1AnimateEpisodeInfoSerializer
    queryset = Anime1AnimateEpisodeInfoModel.objects.select_related('owner').all()
    my_tags = ['Anime1動漫集數資料']

    def list(self, request, *args, **kwargs):
        model = Anime1AnimateEpisodeInfoModel.objects.filter(owner_id=kwargs.get('animate_id'))
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Anime1AnimateEpisodeInfoSerializer(model, many=True)
        return Response(serializer.data)


@method_decorator(**Anime1AnimateEpisodeDoneSwagger.rs)
class Anime1AnimateEpisodeDoneView(BaseAnimateEpisodeDone):
    serializer_class = Anime1AnimateInfoSerializer
    queryset = Anime1AnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination
    animate_info_model = Anime1AnimateInfoModel
    animate_episode_info_model = Anime1AnimateEpisodeInfoModel
    my_tags = ['Anime1動漫下載完畢資料']


@method_decorator(**Anime1MenuSeasonSwagger.rs)
class Anime1MenuSeasonView(ModelViewSet):
    my_tags = ['Anime1首頁季番名稱與網址']

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        data = Anime1.get_home_season_url()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(**Anime1SeasonSwagger.rs)
class Anime1SeasonView(ModelViewSet):
    my_tags = ['Anime1季番資料']

    @method_decorator(cache_page(300))
    def list(self, request, season, *args, **kwargs):
        data = Anime1.get_season_list(season=season)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(**Anime1DestroyManyAnimateSwagger.d)
class Anime1DestroyManyAnimateView(ModelViewSet):
    my_tags = ['Anime1 刪除多筆動漫']

    def destroy(self, request, *args, **kwargs):
        delete_list = request.data.get('deleteArray')
        DB.Anime1.delete_animate_episode(id__in=delete_list)
        DB.My.create_log(msg='Anime1 刪除已選取動漫', action='delete')
        return Response(status=status.HTTP_204_NO_CONTENT)
