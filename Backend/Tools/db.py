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

    @classmethod
    def update_or_create_animate_info(cls, data, image):
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

    @classmethod
    def many_create_animate_episode(cls, data, parent_model):
        models = []
        for episode in data['video']:
            models.append(AnimateEpisodeInfoModel.objects.get_or_create(name=episode['name'], defaults={
                'name': episode['name'],
                'url': episode['url'],
                'owner': parent_model,
            })[0])
        return models

    @classmethod
    @database_sync_to_async
    def many_animate_episode_update_download(cls, pk_list):
        models = []
        for pk in pk_list:
            model = AnimateEpisodeInfoModel.objects.get(pk=pk)
            model.download = True
            model.save()
            models.append(model)
        return models

    @classmethod
    @database_sync_to_async
    def many_animate_episode_ts(cls, data):
        for uri in data:
            AnimateEpisodeTsModel.objects.get_or_create(uri=uri, )


class DB:
    Myself = MyselfBase
