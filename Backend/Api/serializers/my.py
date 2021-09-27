from rest_framework import serializers

from Database.models import HistoryModel, LogModel


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = LogModel
        fields = '__all__'
