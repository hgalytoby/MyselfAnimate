import asyncio

from channels.db import database_sync_to_async
from rest_framework.utils import json

from Tools.db import DB
import copy

from Tools.myself import Myself
from Tools.urls import MyselfFinishAnimateUrl, MyselfFinishAnimateBaseUrl


class Base:
    async def download_tasks(self):
        """
        將現在正要下載的動漫資料傳給前端。
        :return:
        """
        temp = None
        while True:
            if temp != getattr(self.manage, 'download_list') + getattr(self.manage, 'wait_download_list'):
                temp = copy.deepcopy(self.manage.download_list + self.manage.wait_download_list)
                await self.parent.send(
                    text_data=json.dumps({
                        'msg': 'now download array',
                        'data': getattr(self.manage, 'download_list') + getattr(self.manage, 'wait_download_list'),
                        'action': self.task_action}))
            await asyncio.sleep(0.1)


class MyselfManage(Base):
    task_action = 'download_myself_animate_array'

    def __init__(self, parent, manage):
        self.parent = parent
        self.manage = manage

    async def _finish_animate_update(self, *args, **kwargs):
        await self.parent.send(text_data=json.dumps({'msg': f'正在更新中', 'action': kwargs['action'], 'updating': True}))
        await DB.My.create_log(msg='Myself 更新完結動漫', action='update')
        await DB.My.save_settings_update_false(**kwargs['data'])
        total_page_data = await Myself.finish_animate_total_page(url=MyselfFinishAnimateUrl, get_res_text=True)
        for page in range(1, total_page_data['total_page'] + 1):
            if page == 1:
                page_data = await Myself.finish_animate_page_data(url=MyselfFinishAnimateBaseUrl.format(page),
                                                                  res_text=total_page_data['res_text'])
            else:
                page_data = await Myself.finish_animate_page_data(url=MyselfFinishAnimateBaseUrl.format(page))
            await DB.Myself.create_many_finish_animate(data=page_data)
        await DB.My.save_settings(**kwargs['data'])
        await DB.My.create_log(msg='Myself 完結動漫更新完成', action='updated')
        await self.parent.send(
            text_data=json.dumps({'msg': '更新完成', 'action': kwargs['action'], 'updating': False}))

    async def finish_animate_update(self, *args, **kwargs):
        """
        更新完結動漫。
        :return:
        """
        asyncio.create_task(self._finish_animate_update(*args, **kwargs))

    async def animate_download(self, *args, **kwargs):
        """
        下載動漫集數。
        :param data: dict -> 前端傳來要下載動漫的資料。
        :return:
        """
        await self.parent.send(
            text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': kwargs['action'], 'updating': True}))
        try:
            if kwargs['episodes']:
                await DB.My.create_log(msg='Myself 下載動漫', action='download')
                try:
                    download_models = await DB.Myself.create_many_download_models(owner_id_list=kwargs['episodes'])
                    download_data_list = await DB.Myself.get_download_animate_episode_data_list(
                        download_models=download_models)
                    self.manage.wait_download_list.extend(download_data_list)
                except Exception as error:
                    print(error)
                # print(animate_episode_list, '123')
                await self.parent.send(
                    text_data=json.dumps({'msg': '下載完成', 'action': kwargs['action'], 'updating': False}))
        except Exception as e:
            print(e)

    async def search_animate(self, *args, **kwargs):
        """
        搜尋動漫。
        :param data: dict -> 前端傳來要搜尋動漫的資料。
        :return:
        """
        settings_model = await DB.My.get_last_settings()
        if settings_model.myself_finish_animate_update:
            if kwargs['msg']:
                await DB.My.create_log(msg=f'Myself 搜尋{kwargs["msg"]}動漫', action='search')
                model = await DB.Myself.filter_finish_animate(name__contains=kwargs['msg'])
            else:
                await DB.My.create_log(msg=f'Myself 搜尋動漫', action='search')
                model = await DB.Myself.All_finish_animate()
            serializer_data = await DB.Myself.search_finish_animate_paginator(model=model, page=kwargs.get('page'))
            await self.parent.send(text_data=json.dumps({'data': serializer_data, 'action': kwargs['action']}))

    async def clear_finish_animate(self, *args, **kwargs):
        """
        清除已完成下載動漫資料。
        :param data: dict -> 前端傳來要清除已完成下載動漫資料。
        :return:
        """
        print(kwargs)
        await DB.Myself.delete_download_finish_animate()
        await DB.My.create_log(msg='Myself 清除下載已完成', action='delete')
        await self.manage.clear_finish_animate_list()
        await self.parent.send(text_data=json.dumps({'msg': '已清除已完成動漫', 'action': kwargs['action']}))

    async def delete_download_animate(self, *args, **kwargs):
        """
        刪除正在下載動漫資料。
        :param data: dict -> 前端傳來要刪除正在下載動漫資料。
        :return:
        """
        DB.Cache.clear_cache()
        print(kwargs)
        await DB.Myself.delete_download_and_ts(download_model__id__in=kwargs['deletes'])
        await DB.My.create_log(msg='Myself 刪除已選取動漫', action='delete')
        await self.manage.delete_download_animate_list(kwargs['deletes'])
        await self.parent.send(text_data=json.dumps({'msg': '已取消勾選的下載動漫', 'action': kwargs['action']}))

    async def download_order(self, *args, **kwargs):
        """
        更改動漫下載順序。
        :param data: data: dict -> 前端傳來要更改動漫下載順序。
        :return:
        """
        await self.manage.switch_download_order(data=kwargs)
        await DB.My.create_log(msg='Myself 已更新下載順序', action='switch')
        await self.parent.send(text_data=json.dumps({'msg': '已更新下載順序', 'action': kwargs['action']}))


class Anime1Manage(Base):
    task_action = 'download_anime1_animate_array'

    def __init__(self, parent, manage):
        self.parent = parent
        self.manage = manage

    async def animate_download(self, *args, **kwargs):
        """
        下載動漫集數。
        :param data: dict -> 前端傳來要下載動漫的資料。
        :return:
        """
        await self.parent.send(
            text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': kwargs['action'], 'updating': True}))
        try:
            if kwargs['episodes']:
                await DB.My.create_log(msg='Anime1 下載動漫', action='download')
                try:
                    download_models = await DB.Anime1.create_many_download_models(owner_id_list=kwargs['episodes'])
                    download_data_list = await DB.Anime1.get_download_animate_episode_data_list(
                        download_models=download_models)
                    print('download_data_list', download_data_list)
                    self.manage.wait_download_list.extend(download_data_list)
                except Exception as e:
                    print(e)
                print(kwargs['episodes'])
        except Exception as e:
            print(e)

    async def clear_finish_animate(self, *args, **kwargs):
        """
        清除已完成下載動漫資料。
        :param data: dict -> 前端傳來要清除已完成下載動漫資料。
        :return:
        """
        print(kwargs)
        await DB.Anime1.delete_download_finish_animate()
        await DB.My.create_log(msg='Anime1 清除下載已完成', action='delete')
        await self.manage.clear_finish_animate_list()
        await self.parent.send(text_data=json.dumps({'msg': '已清除已完成動漫', 'action': kwargs['action']}))

    async def delete_download_animate(self, *args, **kwargs):
        """
        刪除正在下載動漫資料。
        :param data: dict -> 前端傳來要刪除正在下載動漫資料。
        :return:
        """
        DB.Cache.clear_cache()
        await DB.Anime1.delete_download(download_model__id__in=kwargs['deletes'])
        await DB.My.create_log(msg='Anime1 刪除已選取動漫', action='delete')
        await self.manage.delete_download_animate_list(kwargs['deletes'])
        await self.parent.send(text_data=json.dumps({'msg': '已取消勾選的下載動漫', 'action': kwargs['action']}))

    async def download_order(self, *args, **kwargs):
        """
        更改動漫下載順序。
        :param data: data: dict -> 前端傳來要更改動漫下載順序。
        :return:
        """
        await self.manage.switch_download_order(data=kwargs)
        await DB.My.create_log(msg='Myself 已更新下載順序', action='switch')
        await self.parent.send(text_data=json.dumps({'msg': '已更新下載順序', 'action': kwargs['action']}))
