from rest_framework import serializers

from Api.serializers.base import BaseEpisodeInfoSerializer
from Database.models import Anime1AnimateInfoModel, Anime1AnimateEpisodeInfoModel


class Anime1AnimateEpisodeInfoSerializer(BaseEpisodeInfoSerializer):
    class Meta:
        model = Anime1AnimateEpisodeInfoModel
        exclude = ('owner', )


class Anime1AnimateInfoSerializer(serializers.ModelSerializer):
    episode_info_model = Anime1AnimateEpisodeInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Anime1AnimateInfoModel
        fields = '__all__'
