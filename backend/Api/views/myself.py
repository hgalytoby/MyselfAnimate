from urllib.parse import unquote

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from Api.serializers import MyselfFinishAnimateSerializer, MyselfAnimateEpisodeInfoSerializer, \
    MyselfAnimateInfoSerializer, MyselfDownloadSerializer
from Api.views.base import BaseAnimateEpisodeDone
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
    def get(self, request):
        if not request.query_params.get('url'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        animate_url = unquote(request.query_params.get('url'))
        if 'myself-bbs.com/' in animate_url:
            animate_url = request.query_params.get('url').split('myself-bbs.com/')[1]
        data = DB.Cache.get_cache_data(key=animate_url)
        if data:
            model = DB.Myself.get_animate_info(url=data['url'])
        else:
            data = Myself.animate_info(url=f'{MyselfUrl}{animate_url}')
            if not data or not data.get('image'):
                raise ValueError
            DB.Cache.set_cache_data(key=animate_url, data=data, timeout=1800)
            image = req_bytes(url=data.pop('image'))
            video = data.pop('video')
            model = DB.Myself.update_or_create_animate_info_model(data=data, image=image)
            DB.Myself.create_many_animate_episode(video, owner=model)
        serializer = MyselfAnimateInfoSerializer(model)
        return Response(serializer.data)


class MyselfUrlAnimate(MyselfAnimateInfoView):
    def get(self, request):
        try:
            if not request.query_params.get('url'):
                raise ValueError
            super(MyselfUrlAnimate, self).get(request)
            return Response({
                'result': True,
                'url': request.query_params.get('url')
            })
        except (ValueError, TypeError):
            return Response({
                'result': False,
                'url': request.query_params.get('url')
            })


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

    def list(self, request, *args, **kwargs):
        settings = DB.My.get_or_create_settings()
        if settings.myself_finish_animate_update:
            return super(MyselfFinishAnimateView, self).list(request, *args, **kwargs)
        return Response({})


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


class MyselfAnimateEpisodeDoneView(BaseAnimateEpisodeDone):
    serializer_class = MyselfAnimateInfoSerializer
    queryset = MyselfAnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination
    animate_info_model = MyselfAnimateInfoModel
    animate_episode_info_model = MyselfAnimateEpisodeInfoModel


class MyselfDownloadView(DestroyAPIView):
    serializer_class = MyselfDownloadSerializer
    queryset = MyselfDownloadModel.objects.all()


class MyselfDestroyManyAnimate(APIView):
    def delete(self, request):
        delete_list = request.data.get('deleteArray')
        DB.Myself.delete_animate_episode(id__in=delete_list)
        DB.My.create_log(msg='Myself 刪除已選取動漫', action='delete')
        return Response(status=status.HTTP_204_NO_CONTENT)
