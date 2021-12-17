from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Api.serializers.my import SystemSerializer, HistorySerializer
from Database.models.my import SystemModel, HistoryModel
from Tools.db import DB, MyPageNumberPagination


class SystemView(ListCreateAPIView):
    serializer_class = SystemSerializer
    queryset = SystemModel.objects.all()
    pagination_class = MyPageNumberPagination


class HistoryView(ListAPIView):
    serializer_class = HistorySerializer
    queryset = HistoryModel.objects.all()
    pagination_class = MyPageNumberPagination


class LogView(APIView):
    def get(self, request):
        system_data = DB.My.get_custom_log_data(model=SystemModel.objects.all(), serializer=SystemSerializer)
        history_data = DB.My.get_custom_log_data(model=HistoryModel.objects.all(), serializer=HistorySerializer)
        return Response({
            'system': system_data,
            'history': history_data,
        })
