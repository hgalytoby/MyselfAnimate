from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Api.serializers.my import MySystemSerializer, MyHistorySerializer, MySettingsSerializer
from Database.models.my import MySystemModel, MyHistoryModel, MySettingsModel
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


class MySettingsView(APIView):
    def get(self, request):
        my_settings = MySettingsModel.objects.all().last()
        serializer = MySettingsSerializer(my_settings)
        return Response(serializer.data)

    def put(self, request):
        my_settings = MySettingsModel.objects.all().last()
        serializer = MySettingsSerializer(my_settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
