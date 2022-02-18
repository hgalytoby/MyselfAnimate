from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Api.serializers.my import MySystemSerializer, MyHistorySerializer, MySettingsSerializer
from Database.models.my import MySystemModel, MyHistoryModel, MySettingsModel
from Tools.db import DB, MyPageNumberPagination
from Tools.swagger import MySettingsSwagger, MyLogSwagger, MyHistorySwagger, MySystemSwagger


@method_decorator(**MySystemSwagger.rs)
class MySystemView(ModelViewSet):
    serializer_class = MySystemSerializer
    queryset = MySystemModel.objects.all()
    pagination_class = MyPageNumberPagination
    my_tags = ['系統紀錄']


@method_decorator(**MyHistorySwagger.rs)
class MyHistoryView(ModelViewSet):
    serializer_class = MyHistorySerializer
    queryset = MyHistoryModel.objects.all()
    pagination_class = MyPageNumberPagination
    my_tags = ['歷史紀錄']


@method_decorator(**MyLogSwagger.rs)
class MyLogView(ModelViewSet):
    my_tags = ['所有日誌']

    def list(self, request, *args, **kwargs):
        system_data = DB.My.get_custom_log_data(model=MySystemModel.objects.all(), serializer=MySystemSerializer)
        history_data = DB.My.get_custom_log_data(model=MyHistoryModel.objects.all(), serializer=MyHistorySerializer)
        return Response({
            'system': system_data,
            'history': history_data,
        })


@method_decorator(**MySettingsSwagger.rs)
@method_decorator(**MySettingsSwagger.u)
class MySettingsView(ModelViewSet):
    my_tags = ['設定']

    def list(self, request, *args, **kwargs):
        my_settings = MySettingsModel.objects.all().last()
        serializer = MySettingsSerializer(my_settings)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        my_settings = MySettingsModel.objects.all().last()
        serializer = MySettingsSerializer(my_settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
