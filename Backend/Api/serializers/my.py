from rest_framework import serializers
from Database.models import HistoryModel, SystemModel


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = SystemModel
        fields = '__all__'


class LogSerializer(serializers.Serializer):
    previous = serializers.BooleanField()
    page = serializers.IntegerField(allow_null=True)
    next = serializers.IntegerField(allow_null=True)
    total_pages = serializers.IntegerField()
    count = serializers.IntegerField()
    data = serializers.ListField()
    range = serializers.ListField()
