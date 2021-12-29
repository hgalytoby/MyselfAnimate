from channels.db import database_sync_to_async
from django.db import models

from project.settings import MEDIA_PATH


def upload_image_path(instance, filename):
    """
    """
    return f'{instance.from_website}/{instance.name}/image/{instance.size}_{filename}'


def upload_ts_path(instance, filename):
    """
    """
    return f'{instance.owner.owner.from_website}/{instance.owner.owner.name}/video/ts/{instance.owner.name}/{filename}'


def upload_video_path(instance, filename):
    """
    """
    return f'{instance.owner.from_website}/{instance.owner.name}/video/{filename}'


class BaseAnimateEpisodeInfoModel(models.Model):
    """
    name: 動漫名字
    url: 影片連結
    done: 是否下載完成
    video: 影片位置
    """
    name = models.CharField(max_length=64)
    url = models.URLField()
    done = models.BooleanField(default=False)
    video = models.FileField(upload_to=upload_video_path, null=True, blank=True)

    class Meta:
        abstract = True

    @database_sync_to_async
    def get_animate_name(self):
        """
        在異步情況下取得動漫名字。
        :return:
        """
        return self.owner.name

    @database_sync_to_async
    def get_from_website(self):
        """
        在異步情況下取得哪個網站的動漫。
        :return:
        """
        return self.owner.from_website


class BaseDownloadModel(models.Model):
    def get_and_add_download_data(self, add_data):
        return {
            'episode_id': self.owner.id,
            'animate_id': self.owner.owner.id,
            'animate_name': self.owner.owner.name,
            'episode_name': self.owner.name,
            'done': self.owner.done,
            'id': self.id,
            'status': '準備下載',
            'video': f'{MEDIA_PATH}{self.owner.video.url}' if self.owner.video else None,
            **add_data,
        }

    class Meta:
        abstract = True
