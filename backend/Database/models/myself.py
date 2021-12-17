from channels.db import database_sync_to_async
from django.db import models
from Database.models.my import upload_image_path, upload_ts_path, upload_video_path


class AnimateInfoModel(models.Model):
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


class FinishAnimateModel(models.Model):
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


class AnimateEpisodeInfoModel(models.Model):
    """
    name: 動漫名字
    url: 影片連結
    done: 是否下載完成
    video: 影片位置
    owner: 關聯
    """
    name = models.CharField(max_length=64)
    url = models.URLField()
    done = models.BooleanField(default=False)
    video = models.FileField(upload_to=upload_video_path, null=True, blank=True)
    owner = models.ForeignKey(AnimateInfoModel, on_delete=models.CASCADE, related_name='episode_info_model')

    class Meta:
        db_table = 'MyselfAnimateEpisodeInfo'

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


class AnimateEpisodeTsModel(models.Model):
    """
    ts_url: ts 檔案連結
    done: 是否完成
    owner: 關聯
    """
    uri = models.CharField(max_length=32)
    done = models.BooleanField(default=False)
    ts = models.FileField(upload_to=upload_ts_path)
    owner = models.ForeignKey(AnimateEpisodeInfoModel, on_delete=models.CASCADE, related_name='ts_model')

    class Meta:
        db_table = 'MyselfAnimateEpisodeTs'


class DownloadModel(models.Model):
    """
    owner: 關聯
    """
    owner = models.OneToOneField(AnimateEpisodeInfoModel, on_delete=models.CASCADE, related_name='download_model')

    class Meta:
        db_table = 'MyselfDownload'
