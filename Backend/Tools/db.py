import io
import asyncio
from django.core.files.images import ImageFile
from django.core.paginator import Paginator
from Api.serializers import FinishAnimateSerializer
from channels.db import database_sync_to_async
from Database.models import FinishAnimateModel, AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel, \
    DownloadModel
from django.core.files.base import ContentFile
from Tools.tools import aiohttp_bytes, use_io_get_image_format, page_range
from project.settings import MEDIA_PATH, BASE_DIR


class MyselfBase:
    @classmethod
    @database_sync_to_async
    def create_finish_animate(cls, animate: dict):
        """
        儲存圖片到資料庫。
        :param animate:
        :return:
        """
        image_type = use_io_get_image_format(animate['image'])
        model = FinishAnimateModel()
        model.name = animate['name']
        model.url = animate['url']
        model.info = animate['info']
        model.image.save(f'{animate["name"]}.{image_type}', ContentFile(animate['image']))

    @classmethod
    async def create_finish_animate_data_task(cls, animate: dict):
        """
        request 預覽圖
        因為我不知道怎麼在 database_sync_to_async 下使用 await，所以我拆成兩個方法來做。
        :param animate:
        :return:
        """
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
    def create_many_animate_episode(video: list, **kwargs):
        """
        新增多個動漫集數。
        :param video:
        :return:
        """
        for episode in video:
            AnimateEpisodeInfoModel.objects.get_or_create(name=episode['name'], **kwargs, defaults={
                'name': episode['name'],
                'url': episode['url'],
                'owner': kwargs.get('owner'),
            })

    @staticmethod
    @database_sync_to_async
    def create_many_animate_episode_ts(ts_list: list, **kwargs):
        """
        新增多個動漫某一集的所有 ts 資料。
        :param ts_list:
        :return:
        """
        models = []
        for ts_uri in ts_list:
            models.append(AnimateEpisodeTsModel(uri=ts_uri, **kwargs))
        AnimateEpisodeTsModel.objects.bulk_create(models)

    @staticmethod
    @database_sync_to_async
    def create_many_download_models(owner_id_list: list) -> list:
        """
        :param owner_id_list:
        :return:
        """
        data = []
        for owner_id in owner_id_list:
            data.append(DownloadModel.objects.create(owner_id=owner_id))
        return data

    @staticmethod
    def update_or_create_animate_info_model(data: dict, image: bytes):
        """
        更新或新增動漫資料。
        :param data:
        :param image:
        :return:
        """
        image_type = use_io_get_image_format(image)
        data['image'] = ImageFile(io.BytesIO(image), name=f'{data["name"]}.{image_type}')
        model, created = AnimateInfoModel.objects.update_or_create(url=data['url'], defaults=data)
        return model

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

    @staticmethod
    @database_sync_to_async
    def get_download_animate_episode_data_list(download_models):
        data = []
        for download_model in download_models:
            ts_models = AnimateEpisodeTsModel.objects.select_related('owner').filter(owner_id=download_model.owner_id)
            ts_count = ts_models.count()
            ts_undone_models = ts_models.filter(done=False)
            ts_undone_count = ts_undone_models.count()
            ts_list = []
            for ts_undone_model in ts_undone_models:
                ts_list.append(ts_undone_model.uri)
            data.append({
                'id': download_model.id,
                'episode_id': download_model.owner.id,
                'animate_id': download_model.owner.owner.id,
                'animate_name': download_model.owner.owner.name,
                'episode_name': download_model.owner.name,
                'done': download_model.owner.done,
                'vpx_url': download_model.owner.url,
                'ts_list': ts_list,
                'ts_count': ts_count,
                'count': ts_count - ts_undone_count,
                'status': '準備下載',
                'video': f'{MEDIA_PATH}{download_model.owner.video.url}' if download_model.owner.video else None
            })
        return data

    @staticmethod
    @database_sync_to_async
    def get_total_download_animate_episode_models() -> list:
        """
        取得多個動漫集數資料與更新成下載中。
        :return:
        """
        return DownloadModel.objects.select_related('owner').select_related('owner__owner').all()

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_ts_count(**kwargs):
        """
        取得動漫某一集 ts 總數量。
        :return:
        """
        return AnimateEpisodeTsModel.objects.filter(**kwargs).count()

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_download_undone_id_list():
        """
        取得正在下載的動漫陣列清單。
        :return:
        """
        data = []
        for model in DownloadModel.objects.all():
            data.append(model.id)
        return data

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_info_model(**kwargs):
        """
        取得動漫單影集資料。
        取得動漫資料 model。
        :return:
        """
        return AnimateEpisodeInfoModel.objects.get(**kwargs)

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_info_downloading_models(**kwargs):
        """
        取得指定動漫有哪些集數正在下載的 model。
        :return:
        """
        return list(AnimateEpisodeInfoModel.objects.filter(download=True, done=False, **kwargs))

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_undone_uri_list(**kwargs):
        """
        取得指定動漫某一集尚未下載的 ts uri 陣列清單。
        :return:
        """
        data = []
        for model in AnimateEpisodeTsModel.objects.filter(done=False, **kwargs):
            data.append(model.uri)
        return data

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_list(**kwargs):
        """
        篩選 ts 檔案並轉成 ffmpeg 合併 ts 需要的 txt 格式。
        :param kwargs:
        :return:
        """
        data = []
        for model in AnimateEpisodeTsModel.objects.filter(**kwargs):
            data.append(f"file '{BASE_DIR}{MEDIA_PATH}/{model.ts}'")
        return data

    @staticmethod
    @database_sync_to_async
    def filter_finish_animate(**kwargs):
        """
        不加 list 有時候會出現 You cannot call this from an async context - use a thread or sync_to_async.
        :param kwargs:
        :return:
        """
        return list(FinishAnimateModel.objects.filter(**kwargs))

    @staticmethod
    @database_sync_to_async
    def delete_download_and_ts(**kwargs):
        """
        刪除 Download 與 TS 的資料庫資料。
        :param kwargs:
        :return:
        """
        models = AnimateEpisodeInfoModel.objects.filter(**kwargs)
        for model in models:
            DownloadModel.objects.filter(owner_id=model.pk).delete()
            AnimateEpisodeTsModel.objects.filter(owner_id=model.pk).delete()
            model.done = False
            model.video = None
            model.save()

    @staticmethod
    @database_sync_to_async
    def All_finish_animate():
        """
        不加 list 有時候會出現 You cannot call this from an async context - use a thread or sync_to_async.
        :return:
        """
        return list(FinishAnimateModel.objects.all())

    @classmethod
    @database_sync_to_async
    def delete_filter_animate_episode_ts(cls, **kwargs):
        """
        刪除動滿某一集所有 ts 資料。
        :return:
        """
        AnimateEpisodeTsModel.objects.filter(**kwargs).delete()

    @classmethod
    @database_sync_to_async
    def delete_download_finish_animate(cls):
        """
        刪除下載已完成動漫。
        :return:
        """
        DownloadModel.objects.filter(owner__done=True).delete()

    @classmethod
    @database_sync_to_async
    def delete_download_animate(cls, **kwargs):
        """
        刪除下載資料庫的資料。
        :return:
        """
        DownloadModel.objects.filter(**kwargs).delete()

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_ts_file(ts_content: bytes, **kwargs):
        """
        儲存動漫某一集的 ts 檔案。
        :param ts_content:
        :return:
        """
        model = AnimateEpisodeTsModel.objects.get(**kwargs)
        model.done = True
        model.ts.save(model.uri, ContentFile(ts_content))

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_video_file(video_path: str, **kwargs):
        """
        儲存動漫某一集的檔案。
        :param video_path:
        :return:
        """
        model = AnimateEpisodeInfoModel.objects.get(**kwargs)
        model.done = True
        model.video = video_path
        model.save()

    @staticmethod
    @database_sync_to_async
    def search_finish_animate_paginator(model, page):
        """
        搜尋完結動漫分頁器。
        :param model:
        :param page:
        :return:
        """
        paginator = Paginator(model, 15)
        pag_obj = paginator.page(page if page else 1)
        serializer = FinishAnimateSerializer(pag_obj, many=True)
        return {
            'previous': pag_obj.previous_page_number() if pag_obj.has_previous() else None,
            'page': pag_obj.number,
            'next': pag_obj.next_page_number() if pag_obj.has_next() else None,
            'total_pages': paginator.num_pages,
            'count': paginator.count,
            'data': serializer.data,
            'range': page_range(page=pag_obj.number, total=paginator.num_pages)
        }

    @staticmethod
    @database_sync_to_async
    def switch_download(switch_data1, switch_data2):
        DownloadModel.objects.filter(pk__in=[switch_data1['id'], switch_data2['id']]).delete()
        switch_data1['id'], switch_data2['id'] = switch_data2['id'], switch_data1['id']
        DownloadModel.objects.create(pk=switch_data1['id'], owner_id=switch_data1['episode_id'])
        DownloadModel.objects.create(pk=switch_data2['id'], owner_id=switch_data2['episode_id'])


class DB:
    Myself = MyselfBase
