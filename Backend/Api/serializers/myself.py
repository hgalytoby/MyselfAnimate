from rest_framework import serializers

from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel


class FinishAnimateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return f'http://127.0.0.1:8000/static/uploads{instance.image.url}'

    class Meta:
        model = FinishAnimateModel
        fields = ('id', 'name', 'url', 'image')


class AnimateEpisodeInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)

    class Meta:
        model = AnimateEpisodeInfoModel
        fields = ('id', 'name', 'url', 'download', 'done')