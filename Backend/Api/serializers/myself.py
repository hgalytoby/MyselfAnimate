from rest_framework import serializers

from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel, AnimateInfoModel


class FinishAnimateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return f'http://127.0.0.1:8000/static/uploads{instance.image.url}'

    class Meta:
        model = FinishAnimateModel
        fields = ('id', 'name', 'url', 'image', 'info')


class AnimateEpisodeInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)

    class Meta:
        model = AnimateEpisodeInfoModel
        fields = ('id', 'name', 'url', 'download', 'done')


class AnimateInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    episode_info_model = AnimateEpisodeInfoSerializer(many=True, read_only=True)

    def get_image(self, instance):
        return f'http://127.0.0.1:8000/static/uploads{instance.image.url}'

    class Meta:
        model = AnimateInfoModel
        fields = '__all__'
