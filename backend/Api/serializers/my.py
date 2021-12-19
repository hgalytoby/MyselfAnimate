from rest_framework import serializers
from Database.models.my import MyHistoryModel, MySystemModel


class MyHistorySerializer(serializers.ModelSerializer):
    download_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = MyHistoryModel
        fields = '__all__'


class MySystemSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = MySystemModel
        fields = '__all__'
