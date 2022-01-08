import io
import asyncio
import json
from typing import Union, List

from django.core.files.images import ImageFile
from django.core.paginator import Paginator
from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from Api.serializers import MyselfFinishAnimateSerializer
from channels.db import database_sync_to_async

from django.core.files.base import ContentFile

from Database.models import MyselfFinishAnimateModel, MyselfAnimateEpisodeInfoModel, MyselfAnimateEpisodeTsModel, \
    MyselfDownloadModel, MyselfAnimateInfoModel, MyHistoryModel, MySystemModel, Anime1AnimateInfoModel, \
    Anime1AnimateEpisodeInfoModel, Anime1DownloadModel, MySettingsModel
from Tools.tools import aiohttp_bytes, use_io_get_image_format
from django.core.cache import caches

from project.settings import MEDIA_PATH, BASE_DIR, DOWNLOAD_MAX_VALUE


class MyPageNumberPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'size'
    max_page_size = 60

    def get_paginated_response(self, data: list):
        return Response(self.get_paginated(page_obj=self.page, paginator=self.page.paginator, data=data))

    @classmethod
    def get_paginated(cls, page_obj, paginator, data: list):
        return {
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'page': page_obj.number,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'total_pages': paginator.num_pages,
            'count': paginator.count,
            'data': data,
            'range': cls.page_range(page=page_obj.number, total=paginator.num_pages)
        }

    @staticmethod
    def page_range(page: int, total: int, page_item: int = 10):
        quotient, remainder = divmod(page, page_item)
        print(f'page: {page}, total: {total}')
        remainder_x_page_item = quotient * page_item
        if remainder == 0:
            return list(range((quotient - 1) * page_item + 1, remainder_x_page_item + 1))
        else:
            start = list(range(remainder_x_page_item + 1, remainder_x_page_item + remainder + 1))
            end = remainder_x_page_item + page_item + 1
            if end > total:
                return start + list(range(remainder_x_page_item + remainder + 1, total + 1))
            return start + list(range(remainder_x_page_item + remainder + 1, remainder_x_page_item + page_item + 1))


class Base:
    @classmethod
    @database_sync_to_async
    def switch_download(cls, switch_data1: dict, switch_data2: dict):
        cls.download_model.objects.filter(pk__in=[switch_data1['id'], switch_data2['id']]).delete()
        switch_data1['id'], switch_data2['id'] = switch_data2['id'], switch_data1['id']
        cls.download_model.objects.create(pk=switch_data1['id'], owner_id=switch_data1['episode_id'])
        cls.download_model.objects.create(pk=switch_data2['id'], owner_id=switch_data2['episode_id'])

    @classmethod
    @database_sync_to_async
    def create_many_download_models(cls, owner_id_list: list) -> list:
        """
        :param owner_id_list:
        :return:
        """
        data = []
        for owner_id in owner_id_list:
            data.append(cls.download_model.objects.create(owner_id=owner_id))
        return data

    @classmethod
    @database_sync_to_async
    def get_total_download_animate_episode_models(cls) -> Union[QuerySet, List[MyselfDownloadModel]]:
        """
        取得多個動漫集數資料與更新成下載中。
        :return:
        """
        return cls.download_model.objects.select_related('owner').select_related('owner__owner').all()

    @classmethod
    def get_animate_info(cls, **kwargs):
        return cls.animate_info_model.objects.get(**kwargs)

    @classmethod
    @database_sync_to_async
    def delete_download_finish_animate(cls):
        """
        刪除下載已完成動漫。
        :return:
        """
        cls.download_model.objects.filter(owner__done=True).delete()


class MyselfBase(Base):
    animate_info_model = MyselfAnimateInfoModel
    animate_episode_info_model = MyselfAnimateEpisodeInfoModel
    download_model = MyselfDownloadModel

    @classmethod
    @database_sync_to_async
    def create_finish_animate(cls, animate: dict):
        """
        儲存圖片到資料庫。
        :param animate:
        :return:
        """
        image_type = use_io_get_image_format(animate['image'])
        model = MyselfFinishAnimateModel()
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
            if not await cls.filter_finish_animate(url=animate['url']):
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
            MyselfAnimateEpisodeInfoModel.objects.get_or_create(name=episode['name'], **kwargs, defaults={
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
            models.append(MyselfAnimateEpisodeTsModel(uri=ts_uri, **kwargs))
        MyselfAnimateEpisodeTsModel.objects.bulk_create(models)

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
        model, created = MyselfAnimateInfoModel.objects.update_or_create(url=data['url'], defaults=data)
        return model

    @classmethod
    @database_sync_to_async
    def update_animate_episode_url(cls, new_url: str, model: Union[QuerySet, MyselfAnimateEpisodeInfoModel]):
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
    def get_download_animate_episode_data_list(download_models: Union[QuerySet, List[MyselfDownloadModel]]) -> list:
        result = []
        for download_model in download_models:
            data = {
                **download_model.get_download_data(),
                'vpx_url': download_model.owner.url,
                'ts_count': 100,
                'count': 100,
            }
            if not data['done']:
                ts_models = MyselfAnimateEpisodeTsModel.objects.select_related('owner').filter(
                    owner_id=download_model.owner_id)
                ts_count = ts_models.count()
                ts_undone_models = ts_models.filter(done=False)
                ts_undone_count = ts_undone_models.count()
                ts_list = []
                for ts_undone_model in ts_undone_models:
                    ts_list.append(ts_undone_model.uri)
                data.update({
                    'ts_list': ts_list,
                    'ts_count': ts_count,
                    'count': ts_count - ts_undone_count
                })
            result.append(data)
        return result

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_download_undone_id_list() -> list:
        """
        取得正在下載的動漫陣列清單。
        :return:
        """
        data = []
        for model in MyselfDownloadModel.objects.all():
            data.append(model.id)
        return data

    @staticmethod
    @database_sync_to_async
    def get_animate_episode_info_model(**kwargs) -> Union[QuerySet, MyselfAnimateEpisodeInfoModel]:
        """
        取得動漫單影集資料。
        取得動漫資料 model。
        :return:
        """
        return MyselfAnimateEpisodeInfoModel.objects.select_related('owner').get(**kwargs)

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_info_downloading_models(**kwargs) -> Union[
        QuerySet, List[MyselfAnimateEpisodeInfoModel]]:
        """
        取得指定動漫有哪些集數正在下載的 model。
        :return:
        """
        return list(
            MyselfAnimateEpisodeInfoModel.objects.select_related('owner').filter(done=False, **kwargs))

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_undone_uri_list(**kwargs) -> list:
        """
        取得指定動漫某一集尚未下載的 ts uri 陣列清單。
        :return:
        """
        data = []
        for model in MyselfAnimateEpisodeTsModel.objects.select_related('owner').filter(done=False, **kwargs):
            data.append(model.uri)
        return data

    @staticmethod
    @database_sync_to_async
    def filter_animate_episode_ts_list(**kwargs) -> list:
        """
        篩選 ts 檔案並轉成 ffmpeg 合併 ts 需要的 txt 格式。
        :param kwargs:
        :return:
        """
        data = []
        for model in MyselfAnimateEpisodeTsModel.objects.filter(**kwargs):
            data.append(f"file '{BASE_DIR}{MEDIA_PATH}/{model.ts}'")
        return data

    @staticmethod
    @database_sync_to_async
    def filter_finish_animate(**kwargs) -> Union[QuerySet, List[MyselfFinishAnimateModel]]:
        """
        :param kwargs:
        :return:
        """
        return list(MyselfFinishAnimateModel.objects.filter(**kwargs))

    @staticmethod
    @database_sync_to_async
    def delete_download_and_ts(**kwargs):
        """
        刪除 Download 與 TS 的資料庫資料。
        :param kwargs:
        :return:
        """
        models = MyselfAnimateEpisodeInfoModel.objects.select_related('owner').filter(**kwargs)
        for model in models:
            MyselfDownloadModel.objects.filter(owner_id=model.pk).delete()
            MyselfAnimateEpisodeTsModel.objects.filter(owner_id=model.pk).delete()
            model.done = False
            model.video = None
            model.save()

    @staticmethod
    @database_sync_to_async
    def All_finish_animate() -> Union[QuerySet, List[MyselfFinishAnimateModel]]:
        """
        :return:
        """
        return MyselfFinishAnimateModel.objects.all()

    @classmethod
    @database_sync_to_async
    def delete_filter_animate_episode_ts(cls, **kwargs):
        """
        刪除動滿某一集所有 ts 資料。
        :return:
        """
        MyselfAnimateEpisodeTsModel.objects.filter(**kwargs).delete()

    @classmethod
    @database_sync_to_async
    def delete_download_animate(cls, **kwargs):
        """
        刪除下載資料庫的資料。
        :return:
        """
        MyselfDownloadModel.objects.filter(**kwargs).delete()

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_ts_file(ts_content: bytes, **kwargs):
        """
        儲存動漫某一集的 ts 檔案。
        :param ts_content:
        :return:
        """
        model = MyselfAnimateEpisodeTsModel.objects.get(**kwargs)
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
        model = MyselfAnimateEpisodeInfoModel.objects.get(**kwargs)
        model.done = True
        model.video = video_path
        model.save()

    # TODO 與 MyBase.get_custom_log_data 相似極大以後改善。
    @staticmethod
    @database_sync_to_async
    def search_finish_animate_paginator(model, page: int):
        """
        搜尋完結動漫分頁器。
        :param model:
        :param page:
        :return:
        """
        paginator = Paginator(model, 15)
        page_obj = paginator.page(page if page else 1)
        serializer = MyselfFinishAnimateSerializer(page_obj, many=True)
        return MyPageNumberPagination.get_paginated(page_obj=page_obj, paginator=paginator, data=serializer.data)


class MyBase:
    @staticmethod
    def get_or_create_settings():
        my_settings = MySettingsModel.objects.all().last()
        if not my_settings:
            return MySettingsModel.objects.create(myself_download_value=DOWNLOAD_MAX_VALUE,
                                                  anime1_download_value=DOWNLOAD_MAX_VALUE)
        return my_settings

    @staticmethod
    @database_sync_to_async
    def create_history(**kwargs):
        MyHistoryModel.objects.create(**kwargs)

    @staticmethod
    @database_sync_to_async
    def create_log(msg: str, action: str):
        MySystemModel.objects.create(msg=msg, action=action)

    @staticmethod
    def get_custom_log_data(model, serializer):
        paginator = Paginator(model, 15)
        page_obj = paginator.page(1)
        serializer = serializer(page_obj, many=True)
        return MyPageNumberPagination.get_paginated(page_obj=page_obj, paginator=paginator, data=serializer.data)


class CacheBase:
    cache_db = caches['default']

    @classmethod
    def get_cache_data(cls, key: str):
        return cls.cache_db.get(key)

    @classmethod
    def set_cache_data(cls, key: str, data: str, timeout: int):
        cls.cache_db.set(key, data, timeout=timeout)

    @classmethod
    def clear_cache(cls):
        cls.cache_db.clear()

    @classmethod
    def delete_cache_data(cls, key: str):
        cls.cache_db.delete(key)


class Anime1Base(Base):
    animate_info_model = Anime1AnimateInfoModel
    animate_episode_info_model = Anime1AnimateEpisodeInfoModel
    download_model = Anime1DownloadModel

    @classmethod
    def create_animate_info(cls, **kwargs):
        model, created = Anime1AnimateInfoModel.objects.update_or_create(url=kwargs['url'], defaults=kwargs)
        return model

    # @classmethod
    # def get_animate_info(cls, **kwargs):
    #     return Anime1AnimateInfoModel.objects.get(**kwargs)

    @classmethod
    def update_or_create_many_episode(cls, episodes: list, owner):
        for episode in episodes:
            Anime1AnimateEpisodeInfoModel.objects.update_or_create(name=episode['name'], defaults={
                **episode,
                'owner': owner
            })

    @staticmethod
    @database_sync_to_async
    def get_download_animate_episode_data_list(download_models: Union[QuerySet, List[Anime1DownloadModel]]) -> list:
        result = []
        for download_model in download_models:
            data = {
                **download_model.get_download_data(),
                'url': download_model.owner.url,
                'progress_value': 0,
            }
            result.append(data)
        return result

    @staticmethod
    @database_sync_to_async
    def save_animate_episode_video_file(video_path: str, **kwargs):
        """
        儲存動漫某一集的檔案。
        :param video_path:
        :return:
        """
        model = Anime1AnimateEpisodeInfoModel.objects.get(**kwargs)
        model.done = True
        model.video = video_path
        model.save()

    @staticmethod
    @database_sync_to_async
    def delete_download(**kwargs):
        """
        刪除 Download 的資料庫資料。
        :param kwargs:
        :return:
        """
        models = Anime1AnimateEpisodeInfoModel.objects.select_related('owner').filter(**kwargs)
        for model in models:
            Anime1DownloadModel.objects.filter(owner_id=model.pk).delete()
            model.done = False
            model.video = None
            model.save()


class DB:
    Myself = MyselfBase
    My = MyBase
    Cache = CacheBase
    Anime1 = Anime1Base
