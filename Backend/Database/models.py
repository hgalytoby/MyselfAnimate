from django.db import models


def upload_path(instance, filename):
    """
    Profile name 為資料夾名字放入圖片。
    """
    return f'{instance.from_website}/{instance.name}/{instance.size}_{filename}'


class AnimateWebsiteModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        """
        改資料庫名字。
        """
        db_table = 'AnimateWebsite'


class AnimateInfoModel(models.Model):
    """
    name: 名字
    animate_type: 作品類型
    premiere_date: 首播日期
    episodes: 播放集數
    author: 作者
    remarks: 備註
    small_picture: 小圖
    big_picture: 大圖
    synopsis: 簡介
    """
    size = 'big'
    name = models.CharField(max_length=128)
    animate_type = models.CharField(max_length=32, blank=True, null=True)
    premiere_date = models.CharField(max_length=16, blank=True, null=True)
    episodes = models.CharField(max_length=16, blank=True, null=True)
    author = models.CharField(max_length=32, blank=True, null=True)
    official_website = models.URLField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    from_website = models.ForeignKey(AnimateWebsiteModel, on_delete=models.PROTECT)

    class Meta:
        db_table = 'AnimateInfo'


class FinishAnimateModel(models.Model):
    """
    """
    size = 'small'
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    image = models.ImageField(upload_to=upload_path)
    from_website = models.ForeignKey(AnimateWebsiteModel, on_delete=models.PROTECT)

    class Meta:
        db_table = 'MyselfFinishAnimate'


class AnimateEpisodeInfoModel(models.Model):
    name = models.CharField(max_length=64)
    episode = models.URLField()
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(AnimateInfoModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'AnimateEpisodeInfo'


class AnimateEpisodeTsModel(models.Model):
    ts_url = models.URLField()
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(AnimateEpisodeInfoModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'AnimateEpisodeTs'


class HistoryModel(models.Model):
    animate_website_name = models.CharField(max_length=32)
    animate_name = models.CharField(max_length=128)
    episode_name = models.CharField(max_length=64)
    date = models.DateTimeField()

    class Meta:
        db_table = 'History'
