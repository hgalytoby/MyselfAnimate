from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Tools.anime1 import Anime1
from Tools.urls import Anime1AnimateUrl


class HomeAnimateView(APIView):
    def get(self, request):
        data = Anime1.get_home_animate_data()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnimateInfoView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response(status=status.HTTP_404_NOT_FOUND)
        animate_url = f'{Anime1AnimateUrl}{url}'
        data = Anime1.get_animate_info(animate_url)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
