from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from Api.serializers.myself import FinishAnimateSerializer, AnimateEpisodeInfoSerializer, AnimateInfoSerializer, \
    DownloadSerializer
from Database.models.myself import FinishAnimateModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel, DownloadModel, \
    AnimateInfoModel
from Tools.db import DB, MyPageNumberPagination
from Tools.myself import Myself
from Tools.tools import req_bytes
from Tools.urls import MyselfUrl


class WeekAnimateView(APIView):
    def get(self, request):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnimateInfoView(APIView):
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
        serializer = AnimateInfoSerializer(model)
        return Response(serializer.data)


class FinishListView(APIView):
    def get(self, request):
        data = Myself.finish_list()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FinishAnimateView(ListAPIView):
    serializer_class = FinishAnimateSerializer
    queryset = FinishAnimateModel.objects.all()
    pagination_class = MyPageNumberPagination


class AnimateEpisodeInfoView(RetrieveUpdateAPIView):
    serializer_class = AnimateEpisodeInfoSerializer
    queryset = AnimateEpisodeInfoModel.objects.select_related('owner').all()

    def put(self, request, *args, **kwargs):
        if request.data.get('download'):
            model = AnimateEpisodeInfoModel.objects.get(pk=kwargs.get('pk'))
            AnimateEpisodeTsModel.objects.filter(owner=model).delete()
        return self.update(request, *args, **kwargs)


class AnimateInfoEpisodeView(ListAPIView):
    serializer_class = AnimateEpisodeInfoSerializer
    queryset = AnimateEpisodeInfoModel.objects.select_related('owner').all()

    def list(self, request, *args, **kwargs):
        model = AnimateEpisodeInfoModel.objects.filter(owner_id=kwargs.get('animate_id'))
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AnimateEpisodeInfoSerializer(model, many=True)
        return Response(serializer.data)


class AnimateEpisodeDoneView(ListAPIView):
    serializer_class = AnimateInfoSerializer
    queryset = AnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        prefetch = Prefetch('episode_info_model', queryset=AnimateEpisodeInfoModel.objects.filter(done=True))
        queryset = AnimateInfoModel.objects.prefetch_related(prefetch).filter(episode_info_model__done=True).distinct()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class DownloadView(DestroyAPIView):
    serializer_class = DownloadSerializer
    queryset = DownloadModel.objects.all()
