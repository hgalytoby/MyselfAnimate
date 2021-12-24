from rest_framework import serializers

from Api.serializers.base import BaseEpisodeInfoSerializer
from Database.models import Anime1AnimateInfoModel, Anime1AnimateEpisodeInfoModel


class Anime1EpisodeInfoSerializer(BaseEpisodeInfoSerializer):
    class Meta:
        model = Anime1AnimateEpisodeInfoModel
        fields = ('id', 'name', 'url', 'done', 'video')


class Anime1InfoSerializer(serializers.ModelSerializer):
    episode_info_model = Anime1EpisodeInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Anime1AnimateInfoModel
        fields = '__all__'
