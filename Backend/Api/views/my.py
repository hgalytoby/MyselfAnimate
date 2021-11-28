from rest_framework.generics import ListAPIView, ListCreateAPIView
from Api.serializers import LogSerializer, HistorySerializer
from Api.views.tools import MyPageNumberPagination
from Database.models import LogModel, HistoryModel


class LogView(ListCreateAPIView):
    serializer_class = LogSerializer
    queryset = LogModel.objects.all()
    pagination_class = MyPageNumberPagination


class HistoryView(ListAPIView):
    serializer_class = HistorySerializer
    queryset = HistoryModel.objects.all()
    pagination_class = MyPageNumberPagination
