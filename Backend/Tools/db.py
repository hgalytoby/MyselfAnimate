import io
import asyncio
import subprocess

from PIL import Image
from asgiref.sync import sync_to_async

from Tools.setup import *
from Tools.myself import Myself
from channels.db import database_sync_to_async
from Database.models import FinishAnimateModel, AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from django.core.files.base import ContentFile
from Tools.tools import aiohttp_bytes, use_io_get_image_format, aiohttp_text
from project.settings import MEDIA_PATH


class MyselfBase:
    @classmethod
    @database_sync_to_async
    def create_finish_animate(cls, animate: dict):
        image_type = use_io_get_image_format(animate['image'])
        model = FinishAnimateModel()
        model.name = animate['name']
        model.url = animate['url']
        model.image.save(f'{animate["name"]}.{image_type}', ContentFile(animate['image']))

    @classmethod
    async def create_finish_animate_data_task(cls, animate: dict):
        animate['image'] = await aiohttp_bytes(url=animate['image'])
        await cls.create_finish_animate(animate)

    @classmethod
    async def create_many_finish_animate(cls, data: list):
        """

        :param data:
        :return:
        """
        tasks = []
        for animate in data:
            if not await database_sync_to_async(list)(FinishAnimateModel.objects.filter(url=animate['url'])):
                tasks.append(asyncio.create_task(cls.create_finish_animate_data_task(animate)))
        if tasks:
            await asyncio.wait(tasks)

    @staticmethod
    def update_or_create_animate_info_model(data: dict, image: bytes):
        """
        更新或新增動漫資料。
        :param data:
        :param image:
        :return:
        """
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
    def create_many_animate_episode_models(data: dict, parent_model):
        """
        新增多個動漫集數。
        :param data:
        :param parent_model:
        :return:
        """
        models = []
        for episode in data['video']:
            models.append(
                AnimateEpisodeInfoModel.objects.get_or_create(name=episode['name'], owner=parent_model, defaults={
                    'name': episode['name'],
                    'url': episode['url'],
                    'owner': parent_model,
                })[0])
        return models

    @staticmethod
    @database_sync_to_async
    def get_many_animate_episode_download_data_and_update_download(pk_list: list) -> list:
        """
        取得多個動漫集數資料與更新成下載中。
        :param pk_list:
        :return:
        """
        data = []
        for pk in pk_list:
            model = AnimateEpisodeInfoModel.objects.get(pk=pk)
            model.download = True
            model.save()
            data.append({
                'id': model.id,
                'animate_name': model.owner.name,
                'episode_name': model.name,
                'vpx_url': model.url,
                'count': 0
            })
        return data

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_ts_count(parent_model):
        """
        取得動漫某一集 ts 總數量。
        :param parent_model:
        :return:
        """
        return AnimateEpisodeTsModel.objects.filter(owner=parent_model).count()

    @classmethod
    @database_sync_to_async
    def delete_filter_animate_episode_ts(cls, parent_model):
        """
        刪除動滿某一集所有 ts 資料。
        :param parent_model:
        :return:
        """
        AnimateEpisodeTsModel.objects.filter(owner=parent_model).delete()

    @staticmethod
    @database_sync_to_async
    def create_many_animate_episode_ts(parent_model, ts_list: list):
        """
        新增多個動漫某一集的所有 ts 資料。
        :param parent_model:
        :param ts_list:
        :return:
        """
        models = []
        for ts_uri in ts_list:
            models.append(AnimateEpisodeTsModel(uri=ts_uri, owner=parent_model))
        AnimateEpisodeTsModel.objects.bulk_create(models)

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_ts_file(uri: str, parent_model, ts_content: bytes):
        """
        儲存動漫某一集的 ts 檔案
        :param uri:
        :param parent_model:
        :param ts_content:
        :return:
        """
        model = AnimateEpisodeTsModel.objects.get(uri=uri, owner=parent_model)
        model.done = True
        model.ts.save(uri, ContentFile(ts_content))

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_video_file(name: str, parent_model, video_content: bytes):
        """
        儲存動漫某一集的 ts 檔案
        :param name:
        :param parent_model:
        :param video_content:
        :return:
        """
        model = AnimateEpisodeInfoModel.objects.get(name=name, owner=parent_model)
        model.video.save(f'{model.name}.mp4', ContentFile(video_content))

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_file(pk):
        """
        :return:
        """
        model = AnimateEpisodeInfoModel.objects.get(pk=pk)
        model.done = True
        model.save()

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_download_undone_list():
        """
        取得正在下載的動漫陣列清單。
        :return:
        """
        data = []
        animate_models = AnimateInfoModel.objects.all()
        for animate_model in animate_models:
            episode_ts_models = animate_model.episode_info_model.filter(download=True, done=False)
            if episode_ts_models:
                data.append({'id': animate_model.id, 'name': animate_model.name, 'url': animate_model.url})
        return data

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_info_model(animate_name: str, episode_name: str):
        """
        取得動漫資料 model。
        :param animate_name:
        :param episode_name:
        :return:
        """
        return AnimateEpisodeInfoModel.objects.get(owner__name=animate_name, name=episode_name)

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_info_downloading_models(owner_id):
        """
        取得指定動漫有哪些集數正在下載的 model。
        :param owner_id:
        :return:
        """
        return list(AnimateEpisodeInfoModel.objects.filter(owner_id=owner_id, download=True))

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_undone_uri_list(parent_model):
        """
        取得指定動漫某一集尚未下載的 ts uri 陣列清單。
        :param parent_model:
        :return:
        """
        data = []
        for model in AnimateEpisodeTsModel.objects.filter(owner=parent_model, done=False):
            data.append(model.uri)
        return data

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_undone_ts_list(parent_model):
        data = []
        for model in AnimateEpisodeTsModel.objects.filter(owner=parent_model):
            data.append(f"file '.{MEDIA_PATH}/{model.ts}'")
        return data

    @classmethod
    @database_sync_to_async
    def update_animate_episode_url(cls, new_url: str, model):
        """
        更新 AnimateEpisodeInfoModel 的 URL。
        :param new_url:
        :param model:
        :return:
        """
        model.url = new_url
        model.save()


class DB:
    Myself = MyselfBase


if __name__ == '__main__':
    animate = AnimateInfoModel.objects.last()
    episode_info = AnimateEpisodeInfoModel.objects.filter(owner=animate).first()
    # print(episode_info.id)
    episode_ts = AnimateEpisodeTsModel.objects.filter(owner=episode_info)
    # print(episode_ts)
    data = []
    for index, ts in enumerate(episode_ts):
        data.append(f"file './{MEDIA_PATH}/{ts.ts}'")
        # print(f'.{MEDIA_PATH}/{ts.ts}')

    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))
    # videos = '|'.join(data)
    # print(videos)
    # print(videos)
    # # cmd = f'ffmpeg -i "concat:{videos}" -y -c copy C:/Python/MyselfAnimate/backend/out.mp4'
    # cmd = f'ffmpeg -f concat -safe 0 -y -i file.txt -c copy C:/Python/MyselfAnimate/backend/out.mp4'
    # print(1)
    # run_ffmpeg = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # run_ffmpeg.wait()
    # print(2)
