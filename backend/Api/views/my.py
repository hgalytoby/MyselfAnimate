from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Api.serializers.my import MySystemSerializer, MyHistorySerializer
from Database.models.my import MySystemModel, MyHistoryModel
from Tools.db import DB, MyPageNumberPagination


class MySystemView(ListCreateAPIView):
    serializer_class = MySystemSerializer
    queryset = MySystemModel.objects.all()
    pagination_class = MyPageNumberPagination


class MyHistoryView(ListAPIView):
    serializer_class = MyHistorySerializer
    queryset = MyHistoryModel.objects.all()
    pagination_class = MyPageNumberPagination


class MyLogView(APIView):
    def get(self, request):
        system_data = DB.My.get_custom_log_data(model=MySystemModel.objects.all(), serializer=MySystemSerializer)
        history_data = DB.My.get_custom_log_data(model=MyHistoryModel.objects.all(), serializer=MyHistorySerializer)
        return Response({
            'system': system_data,
            'history': history_data,
        })
