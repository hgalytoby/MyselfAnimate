from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from Api.serializers import FinishAnimateSerializer, AnimateEpisodeInfoSerializer
from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from Tools.db import DB
from Tools.myself import Myself
from Tools.tools import req_bytes
from project.settings import MEDIA_PATH


class WeekAnimateView(APIView):
    def get(self, request):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnimateInfoView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        animate_url = f'https://myself-bbs.com/{url}'
        data = Myself.animate_info(url=animate_url)
        image = req_bytes(url=data['image'])
        model = DB.Myself.update_or_create_animate_info_model(data=data, image=image)
        models = DB.Myself.create_many_animate_episode_models(data, owner=model)
        data['image'] = f'{MEDIA_PATH}{model.image.url}'
        data['id'] = model.id
        data['video'] = [m.to_dict() for m in models]
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FinishListView(APIView):
    def get(self, request):
        data = Myself.finish_list()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FinishAnimateView(ListAPIView):
    serializer_class = FinishAnimateSerializer
    queryset = FinishAnimateModel.objects.all()


class AnimateEpisodeInfoView(RetrieveUpdateAPIView):
    serializer_class = AnimateEpisodeInfoSerializer
    queryset = AnimateEpisodeInfoModel.objects.select_related('owner').all()

    def put(self, request, *args, **kwargs):
        if request.data.get('download'):
            model = AnimateEpisodeInfoModel.objects.get(pk=kwargs.get('pk'))
            AnimateEpisodeTsModel.objects.filter(owner=model).delete()
        return self.update(request, *args, **kwargs)
