from urllib.parse import unquote
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Api.serializers import MyselfFinishAnimateSerializer, MyselfAnimateEpisodeInfoSerializer, \
    MyselfAnimateInfoSerializer
from Api.views.base import BaseAnimateEpisodeDone
from Database.models.myself import MyselfFinishAnimateModel, MyselfAnimateEpisodeInfoModel, \
    MyselfAnimateInfoModel
from Tools.db import DB, MyPageNumberPagination
from Tools.myself import Myself
from Tools.swagger import MyselfWeekAnimateSwagger, MyselfAnimateInfoSwagger, MyselfUrlAnimateSwagger, \
    MyselfFinishListSwagger, MyselfFinishAnimateSwagger, MyselfAnimateEpisodeInfoEpisodeSwagger, \
    MyselfAnimateEpisodeDoneSwagger, MyselfDestroyManyAnimateSwagger
from Tools.tools import req_bytes
from Tools.urls import MyselfUrl


@method_decorator(**MyselfWeekAnimateSwagger.rs)
class MyselfWeekAnimateView(ModelViewSet):
    my_tags = ['Myself 每週動漫資料']

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(**MyselfAnimateInfoSwagger.rs)
class MyselfAnimateInfoView(ModelViewSet):
    my_tags = ['Myself 動漫資料']

    def list(self, request, *args, **kwargs):
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


@method_decorator(**MyselfUrlAnimateSwagger.rs)
class MyselfUrlAnimate(ModelViewSet):
    my_tags = ['Myself 搜尋動漫']

    def list(self, request, *args, **kwargs):
        try:
            if not request.query_params.get('url'):
                raise ValueError
            super(MyselfUrlAnimate, self).list(request, *args, **kwargs)
            return Response({
                'result': True,
                'url': request.query_params.get('url')
            })
        except (ValueError, TypeError):
            return Response({
                'result': False,
                'url': request.query_params.get('url')
            })


@method_decorator(**MyselfFinishListSwagger.rs)
class MyselfFinishListView(ModelViewSet):
    my_tags = ['Myself 完結動漫列表資料']

    @method_decorator(cache_page(300))
    def list(self, request, *args, **kwargs):
        data = Myself.finish_list()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(**MyselfFinishAnimateSwagger.rs)
class MyselfFinishAnimateView(ModelViewSet):
    serializer_class = MyselfFinishAnimateSerializer
    queryset = MyselfFinishAnimateModel.objects.all()
    pagination_class = MyPageNumberPagination
    my_tags = ['Myself 已下載的完結動漫資料']

    def list(self, request, *args, **kwargs):
        settings = DB.My.get_or_create_settings()
        if settings.myself_finish_animate_update:
            return super(MyselfFinishAnimateView, self).list(request, *args, **kwargs)
        return Response({})


@method_decorator(**MyselfAnimateEpisodeInfoEpisodeSwagger.rs)
class MyselfAnimateInfoEpisodeView(ModelViewSet):
    serializer_class = MyselfAnimateEpisodeInfoSerializer
    queryset = MyselfAnimateEpisodeInfoModel.objects.select_related('owner').all()
    my_tags = ['Myself 動漫集數資料']

    def list(self, request, *args, **kwargs):
        model = MyselfAnimateEpisodeInfoModel.objects.filter(owner_id=kwargs.get('animate_id'))
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MyselfAnimateEpisodeInfoSerializer(model, many=True)
        return Response(serializer.data)


@method_decorator(**MyselfAnimateEpisodeDoneSwagger.rs)
class MyselfAnimateEpisodeDoneView(BaseAnimateEpisodeDone):
    serializer_class = MyselfAnimateInfoSerializer
    queryset = MyselfAnimateInfoModel.objects.all()
    pagination_class = MyPageNumberPagination
    animate_info_model = MyselfAnimateInfoModel
    animate_episode_info_model = MyselfAnimateEpisodeInfoModel
    my_tags = ['Myself 動漫下載完畢資料']


@method_decorator(**MyselfDestroyManyAnimateSwagger.d)
class MyselfDestroyManyAnimate(ModelViewSet):
    my_tags = ['Myself 刪除多筆動漫']

    def destroy(self, request, *args, **kwargs):
        delete_list = request.data.get('deleteArray')
        DB.Myself.delete_animate_episode(id__in=delete_list)
        DB.My.create_log(msg='Myself 刪除已選取動漫', action='delete')
        return Response(status=status.HTTP_204_NO_CONTENT)
