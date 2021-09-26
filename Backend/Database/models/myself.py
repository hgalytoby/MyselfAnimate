from django.db import models

from Database.models.basse import upload_path


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
    animate_type = models.CharField(max_length=32, blank=True, null=True)
    premiere_date = models.CharField(max_length=16, blank=True, null=True)
    episode = models.CharField(max_length=16, blank=True, null=True)
    author = models.CharField(max_length=32, blank=True, null=True)
    official_website = models.URLField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'AnimateInfo'


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
    image = models.ImageField(upload_to=upload_path)

    class Meta:
        db_table = 'MyselfFinishAnimate'


class AnimateEpisodeInfoModel(models.Model):
    """
    name: 動漫名字
    episode: 影片連結
    done: 是否完成
    owner: 關聯
    """
    name = models.CharField(max_length=64)
    episode = models.URLField()
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(AnimateInfoModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'AnimateEpisodeInfo'


class AnimateEpisodeTsModel(models.Model):
    """
    ts_url: ts 檔案連結
    done: 是否完成
    owner: 關聯
    """
    ts_url = models.URLField()
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(AnimateEpisodeInfoModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'AnimateEpisodeTs'
