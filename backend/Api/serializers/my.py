from rest_framework import serializers
from Database.models.my import HistoryModel, SystemModel


class HistorySerializer(serializers.ModelSerializer):
    download_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = HistoryModel
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = SystemModel
        fields = '__all__'
