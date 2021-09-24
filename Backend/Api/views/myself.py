from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from Api.serializers import FinishAnimateSerializer
from Database.models import FinishAnimateModel
from Tools.myself import Myself


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

    def list(self, request, *args, **kwargs):
        queryset = FinishAnimateModel.objects.select_related('from_website').all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
