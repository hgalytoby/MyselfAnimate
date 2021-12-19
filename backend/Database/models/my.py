from django.db import models


class MyHistoryModel(models.Model):
    animate_website_name = models.CharField(max_length=32)
    animate_name = models.CharField(max_length=128)
    episode_name = models.CharField(max_length=64)
    download_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MyHistory'
        ordering = ('-download_date',)


class MySystemModel(models.Model):
    msg = models.TextField()
    action = models.CharField(max_length=32)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MySystem'
        ordering = ('-datetime',)


class MyLoveGroupModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'MyLoveGroupModel'
