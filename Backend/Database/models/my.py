from django.db import models


def upload_image_path(instance, filename):
    """
    Profile name 為資料夾名字放入圖片。
    """
    return f'{instance.from_website}/{instance.name}/{instance.size}_{filename}'


def upload_ts_path(instance, filename):
    """
    Profile name 為資料夾名字放入圖片。
    """
    return f'ts/{instance.owner.owner.name}/{instance.owner.name}/{filename}'


def upload_video_path(instance, filename):
    """
    Profile name 為資料夾名字放入圖片。
    """
    return f'video/{instance.owner.name}/{instance.name}/{filename}'


class HistoryModel(models.Model):
    animate_website_name = models.CharField(max_length=32)
    animate_name = models.CharField(max_length=128)
    episode_name = models.CharField(max_length=64)
    download_date = models.DateTimeField()

    class Meta:
        db_table = 'History'


class LogModel(models.Model):
    msg = models.TextField()
    action = models.CharField(max_length=32)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Log'


class LoveGroupModel(models.Model):
    name = models.CharField(max_length=32)
