from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Database.models import AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from django.views import View


class TestView(APIView):
    def get(self, request):
        # model = AnimateEpisodeInfoModel.objects.get(pk=121)
        data = []
        # for m in AnimateEpisodeTsModel.objects.filter(owner=model):
        #     data.append(m.uri)
        # print(data)
        for m in AnimateEpisodeTsModel.objects.filter(owner__name='第 01 話', owner__owner__name='遊戲人生 劇場版／遊戲人生 ZERO'):
            data.append(m.uri)
        print(data)
        return Response({}, status=status.HTTP_200_OK)
