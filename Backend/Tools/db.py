import io
import asyncio
from PIL import Image
from asgiref.sync import sync_to_async

from Tools.setup import *
from channels.db import database_sync_to_async
from Database.models import FinishAnimateModel, AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from django.core.files.base import ContentFile
from Tools.tools import aiohttp_bytes, use_io_get_image_format


class MyselfBase:
    @classmethod
    @database_sync_to_async
    def create_finish_animate(cls, animate):
        image_type = use_io_get_image_format(animate['image'])
        model = FinishAnimateModel()
        model.name = animate['name']
        model.url = animate['url']
        model.image.save(f'{animate["name"]}.{image_type}', ContentFile(animate['image']))

    @classmethod
    async def create_finish_animate_data_task(cls, animate):
        animate['image'] = await aiohttp_bytes(url=animate['image'])
        await cls.create_finish_animate(animate)

    @classmethod
    async def create_many_finish_animate(cls, data):
        tasks = []
        for animate in data:
            if not await database_sync_to_async(list)(FinishAnimateModel.objects.filter(url=animate['url'])):
                tasks.append(asyncio.create_task(cls.create_finish_animate_data_task(animate)))
        if tasks:
            await asyncio.wait(tasks)

    @staticmethod
    def update_or_create_animate_info(data, image):
        try:
            model = AnimateInfoModel.objects.get(url=data['url'])
        except AnimateInfoModel.DoesNotExist:
            model = AnimateInfoModel()
        image_type = use_io_get_image_format(image)
        for k, v in data.items():
            if k != 'image':
                setattr(model, k, v)
        model.image.delete(save=True)
        model.image.save(f'{data["name"]}.{image_type}', ContentFile(image))
        return model

    @staticmethod
    def many_create_animate_episode(data, parent_model):
        models = []
        for episode in data['video']:
            models.append(AnimateEpisodeInfoModel.objects.get_or_create(name=episode['name'], defaults={
                'name': episode['name'],
                'url': episode['url'],
                'owner': parent_model,
            })[0])
        return models

    @staticmethod
    @database_sync_to_async
    def many_animate_episode_update_download(pk_list):
        models = []
        for pk in pk_list:
            model = AnimateEpisodeInfoModel.objects.get(pk=pk)
            model.download = True
            model.save()
            models.append(model)
        return models

    @staticmethod
    @database_sync_to_async
    def many_get_or_create_animate_episode_ts(data):
        for uri in data:
            AnimateEpisodeTsModel.objects.get_or_create(uri=uri, )

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_ts_count(model):
        return AnimateEpisodeTsModel.objects.filter(owner=model).count()

    @staticmethod
    @database_sync_to_async
    def delete_filter_animate_episode_ts(model):
        AnimateEpisodeTsModel.objects.filter(owner=model).delete()

    @staticmethod
    @database_sync_to_async
    def many_create_animate_episode_ts(model, m3u8_obj):
        models = []
        for obj in m3u8_obj.segments:
            models.append(AnimateEpisodeTsModel(uri=obj.uri, owner=model))
        AnimateEpisodeTsModel.objects.bulk_create(models)


class DB:
    Myself = MyselfBase
