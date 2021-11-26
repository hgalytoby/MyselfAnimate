from rest_framework.generics import ListAPIView, ListCreateAPIView
from Api.serializers import LogSerializer, HistorySerializer
from Database.models import LogModel, HistoryModel


class LogView(ListCreateAPIView):
    serializer_class = LogSerializer
    queryset = LogModel.objects.all()


class HistoryView(ListAPIView):
    serializer_class = HistorySerializer
    queryset = HistoryModel.objects.all()
