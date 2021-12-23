from rest_framework import serializers
from Database.models.myself import MyselfFinishAnimateModel, MyselfAnimateEpisodeInfoModel, MyselfAnimateInfoModel, \
    MyselfDownloadModel


class MyselfFinishAnimateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return f'/static/uploads{instance.image.url}'

    class Meta:
        model = MyselfFinishAnimateModel
        fields = ('id', 'name', 'url', 'image', 'info')


class MyselfAnimateEpisodeInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    video = serializers.SerializerMethodField()

    def get_video(self, instance):
        if instance.video:
            return f'/static/uploads{instance.video.url}'
        return None

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
