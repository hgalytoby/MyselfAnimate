from django.db import models
from Database.models.base import BaseAnimateEpisodeInfoModel, BaseDownloadModel


class Anime1AnimateInfoModel(models.Model):
    """
    from_website: 從哪個網站
    name: 動漫名字
    url: 動漫網址
    episode: 播放集數
    years: 年份
    season: 作者
    subtitle_group: 字幕組
    """
    from_website = 'Anime1'
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    episode = models.CharField(max_length=16)
    years = models.CharField(max_length=8)
    season = models.CharField(max_length=32)
    subtitle_group = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'Anime1AnimateInfo'


class Anime1AnimateEpisodeInfoModel(BaseAnimateEpisodeInfoModel):
    """
    owner: 關聯
    """
    owner = models.ForeignKey(Anime1AnimateInfoModel, on_delete=models.CASCADE, related_name='episode_info_model')
    published_updated_date = models.DateField()
    updated = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Anime1AnimateEpisodeInfo'
        ordering = ('-published_updated_date', )


class Anime1DownloadModel(BaseDownloadModel):
    """
    owner: 關聯
    """
    owner = models.OneToOneField(Anime1AnimateEpisodeInfoModel, on_delete=models.CASCADE, related_name='download_model')

    class Meta:
        db_table = 'Anime1Download'
