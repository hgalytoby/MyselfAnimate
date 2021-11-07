from rest_framework import serializers

from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel, AnimateInfoModel, DownloadModel


class FinishAnimateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return f'/static/uploads{instance.image.url}'

    class Meta:
        model = FinishAnimateModel
        fields = ('id', 'name', 'url', 'image', 'info')


class AnimateEpisodeInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    video = serializers.SerializerMethodField()

    def get_video(self, instance):
        if instance.video:
            return f'/static/uploads{instance.video.url}'
        return None

    class Meta:
        model = AnimateEpisodeInfoModel
        fields = ('id', 'name', 'url', 'done', 'video')


class AnimateInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    episode_info_model = AnimateEpisodeInfoSerializer(many=True, read_only=True)

    def get_image(self, instance):
        return f'/static/uploads{instance.image.url}'

    class Meta:
        model = AnimateInfoModel
        fields = '__all__'


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadModel
        fields = ('id',)
