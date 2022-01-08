from rest_framework import serializers
from Database.models.my import MyHistoryModel, MySystemModel, MySettingsModel


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


class MySettingsSerializer(serializers.ModelSerializer):
    myself_download_value = serializers.IntegerField(min_value=1, max_value=30)
    anime1_download_value = serializers.IntegerField(min_value=1, max_value=30)

    class Meta:
        model = MySettingsModel
        fields = '__all__'
