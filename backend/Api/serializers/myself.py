from rest_framework import serializers

from Api.serializers.base import BaseEpisodeInfoSerializer
from Database.models.myself import MyselfFinishAnimateModel, MyselfAnimateEpisodeInfoModel, MyselfAnimateInfoModel, \
    MyselfDownloadModel


class MyselfFinishAnimateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return f'/static/uploads{instance.image.url}'

    class Meta:
        model = MyselfFinishAnimateModel
        fields = ('id', 'name', 'url', 'image', 'info')


class MyselfAnimateEpisodeInfoSerializer(BaseEpisodeInfoSerializer):
    class Meta:
        model = MyselfAnimateEpisodeInfoModel
        fields = ('id', 'name', 'url', 'done', 'video')


class MyselfAnimateInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    episode_info_model = MyselfAnimateEpisodeInfoSerializer(many=True, read_only=True)

    def get_image(self, instance):
        return f'/static/uploads{instance.image.url}'

    class Meta:
        model = MyselfAnimateInfoModel
        fields = '__all__'


class MyselfDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyselfDownloadModel
        fields = ('id',)
