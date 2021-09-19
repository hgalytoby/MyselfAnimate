from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Tools.MyselfTool import Myself


class WeekAnimateView(APIView):
    def get(self, request):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
