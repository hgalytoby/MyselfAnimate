from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Tools.anime1 import Anime1


class HomeAnimateView(APIView):
    def get(self, request):
        data = Anime1.get_home_animate_data()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
