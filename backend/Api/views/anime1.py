from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Api.serializers import Anime1AnimateEpisodeInfoSerializer, Anime1AnimateInfoSerializer
from Database.models import Anime1AnimateEpisodeInfoModel, Anime1AnimateInfoModel
from Tools.anime1 import Anime1
from Tools.db import DB, MyPageNumberPagination
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
        if data:
            return Response(data, status=status.HTTP_200_OK)
        if request.data:
            model = DB.Anime1.create_animate_info(**request.data)
        else:
            model = DB.Anime1.get_animate_info(url=url)
        episode_data = Anime1.get_animate_info(url=animate_url, data=[])
        DB.Anime1.update_or_create_many_episode(episodes=episode_data, owner=model)
        serializer = Anime1AnimateInfoSerializer(model)
        DB.Cache.set_cache_data(key=animate_url, data=serializer.data, timeout=1800)
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


class Anime1AnimateEpisodeDoneView(ListAPIView):
    serializer_class = Anime1AnimateInfoSerializer
    queryset = Anime1AnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        prefetch = Prefetch('episode_info_model', queryset=Anime1AnimateEpisodeInfoModel.objects.filter(done=True))
        queryset = Anime1AnimateInfoModel.objects.prefetch_related(prefetch).filter(
            episode_info_model__done=True).distinct()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
