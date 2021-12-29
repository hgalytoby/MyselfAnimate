from django.db import models
from Database.models.base import upload_image_path, upload_ts_path, BaseAnimateEpisodeInfoModel, BaseDownloadModel


class MyselfAnimateInfoModel(models.Model):
    """
    size: 存圖時要定義的名稱
    from_website: 從哪個網站
    name: 動漫名字
    animate_type: 作品類型
    premiere_date: 首播日期
    episode: 播放集數
    author: 作者
    official_website: 官方網站
    remarks: 備註
    image: 預覽圖
    synopsis: 簡介
    """
    size = 'big'
    from_website = 'Myself'
    name = models.CharField(max_length=128)
    animate_type = models.CharField(max_length=32)
    premiere_date = models.CharField(max_length=16)
    episode = models.CharField(max_length=16)
    author = models.CharField(max_length=32)
    official_website = models.URLField()
    remarks = models.CharField(max_length=64)
    image = models.ImageField(upload_to=upload_image_path)
    synopsis = models.TextField()
    url = models.URLField(unique=True)

    class Meta:
        db_table = 'MyselfAnimateInfo'


class MyselfFinishAnimateModel(models.Model):
    """
    size: 存圖時要定義的名稱
    from_website: 從哪個網站
    name: 動漫名字
    url: 網站連結
    image: 預覽圖
    """
    size = 'small'
    from_website = 'Myself'
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    image = models.ImageField(upload_to=upload_image_path)
    info = models.CharField(max_length=16)

    class Meta:
        db_table = 'MyselfFinishAnimate'


class MyselfAnimateEpisodeInfoModel(BaseAnimateEpisodeInfoModel):
    """
    owner: 關聯
    """
    owner = models.ForeignKey(MyselfAnimateInfoModel, on_delete=models.CASCADE, related_name='episode_info_model')

    class Meta:
        db_table = 'MyselfAnimateEpisodeInfo'


class MyselfAnimateEpisodeTsModel(models.Model):
    """
    ts_url: ts 檔案連結
    done: 是否完成
    owner: 關聯
    """
    uri = models.CharField(max_length=32)
    done = models.BooleanField(default=False)
    ts = models.FileField(upload_to=upload_ts_path)
    owner = models.ForeignKey(MyselfAnimateEpisodeInfoModel, on_delete=models.CASCADE, related_name='ts_model')

    class Meta:
        db_table = 'MyselfAnimateEpisodeTs'


class MyselfDownloadModel(BaseDownloadModel):
    """
    owner: 關聯
    """
    owner = models.OneToOneField(MyselfAnimateEpisodeInfoModel, on_delete=models.CASCADE, related_name='download_model')

    class Meta:
        db_table = 'MyselfDownload'
