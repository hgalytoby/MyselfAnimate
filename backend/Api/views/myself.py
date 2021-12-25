from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from Api.serializers import MyselfFinishAnimateSerializer, MyselfAnimateEpisodeInfoSerializer, \
    MyselfAnimateInfoSerializer, MyselfDownloadSerializer
from Database.models.myself import MyselfFinishAnimateModel, MyselfAnimateEpisodeInfoModel, MyselfAnimateEpisodeTsModel, \
    MyselfDownloadModel, MyselfAnimateInfoModel
from Tools.db import DB, MyPageNumberPagination
from Tools.myself import Myself
from Tools.tools import req_bytes
from Tools.urls import MyselfUrl


class MyselfWeekAnimateView(APIView):
    @method_decorator(cache_page(300))
    def get(self, request):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class MyselfAnimateInfoView(APIView):
    # @method_decorator(cache_page(1800))
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response(status=status.HTTP_404_NOT_FOUND)
        animate_url = f'{MyselfUrl}{url}'
        data = Myself.animate_info(url=animate_url)
        image = req_bytes(url=data['image'])
        video = data.pop('video')
        model = DB.Myself.update_or_create_animate_info_model(data=data, image=image)
        DB.Myself.create_many_animate_episode(video, owner=model)
        serializer = MyselfAnimateInfoSerializer(model)
        return Response(serializer.data)


class MyselfFinishListView(APIView):
    @method_decorator(cache_page(300))
    def get(self, request):
        data = Myself.finish_list()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class MyselfFinishAnimateView(ListAPIView):
    serializer_class = MyselfFinishAnimateSerializer
    queryset = MyselfFinishAnimateModel.objects.all()
    pagination_class = MyPageNumberPagination


class MyselfAnimateEpisodeInfoView(RetrieveUpdateAPIView):
    serializer_class = MyselfAnimateEpisodeInfoSerializer
    queryset = MyselfAnimateEpisodeInfoModel.objects.select_related('owner').all()

    def put(self, request, *args, **kwargs):
        if request.data.get('download'):
            model = MyselfAnimateEpisodeInfoModel.objects.get(pk=kwargs.get('pk'))
            MyselfAnimateEpisodeTsModel.objects.filter(owner=model).delete()
        return self.update(request, *args, **kwargs)


class MyselfAnimateInfoEpisodeView(ListAPIView):
    serializer_class = MyselfAnimateEpisodeInfoSerializer
    queryset = MyselfAnimateEpisodeInfoModel.objects.select_related('owner').all()

    def list(self, request, *args, **kwargs):
        model = MyselfAnimateEpisodeInfoModel.objects.filter(owner_id=kwargs.get('animate_id'))
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MyselfAnimateEpisodeInfoSerializer(model, many=True)
        return Response(serializer.data)


class MyselfAnimateEpisodeDoneView(ListAPIView):
    serializer_class = MyselfAnimateInfoSerializer
    queryset = MyselfAnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        prefetch = Prefetch('episode_info_model', queryset=MyselfAnimateEpisodeInfoModel.objects.filter(done=True))
        queryset = MyselfAnimateInfoModel.objects.prefetch_related(prefetch).filter(
            episode_info_model__done=True).distinct()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class MyselfDownloadView(DestroyAPIView):
    serializer_class = MyselfDownloadSerializer
    queryset = MyselfDownloadModel.objects.all()
