from rest_framework import serializers


class BaseEpisodeInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    video = serializers.SerializerMethodField()

    def get_video(self, instance):
        if instance.video:
            return f'/static/uploads{instance.video.url}'
        return None
