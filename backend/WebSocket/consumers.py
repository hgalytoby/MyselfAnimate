import json
import asyncio
from Tools.db import DB
from Tools.myself import Myself
from Tools.download import MyselfDownloadManage, Anime1DownloadManage
from Tools.urls import MyselfFinishAnimateUrl, MyselfFinishAnimateBaseUrl
from channels.generic.websocket import AsyncWebsocketConsumer

myself_download_manage = MyselfDownloadManage()
anime1_download_manage = Anime1DownloadManage()


class Base:
    async def download_tasks(self):
        """
        將現在正要下載的動漫資料傳給前端。
        :return:
        """
        while True:
            await self.parent.send(
                text_data=json.dumps({
                    'msg': 'now download array',
                    'data': self.download + self.wait,
                    'action': self.task_action}))
            await asyncio.sleep(0.5)


class MyselfManage(Base):
    download = myself_download_manage.download_list
    wait = myself_download_manage.wait_download_list
    task_action = 'download_myself_animate_array'

    def __init__(self, parent):
        self.parent = parent

    async def finish_animate_update(self):
        """
        更新完結動漫。
        :return:
        """
        await DB.My.create_log(msg='Myself 更新完結動漫', action='update')
        total_page_data = await Myself.finish_animate_total_page(url=MyselfFinishAnimateUrl, get_res_text=True)
        for page in range(1, total_page_data['total_page'] + 1):
            if page == 1:
                page_data = await Myself.finish_animate_page_data(url=MyselfFinishAnimateBaseUrl.format(page),
                                                                  res_text=total_page_data['res_text'])
            else:
                page_data = await Myself.finish_animate_page_data(url=MyselfFinishAnimateBaseUrl.format(page))
            await DB.Myself.create_many_finish_animate(data=page_data)

        await DB.My.create_log(msg='Myself 完結動漫更新完成', action='updated')
        await asyncio.sleep(5)
        await self.parent.send(
            text_data=json.dumps({'msg': '更新完成', 'action': 'myself_finish_animate_update', 'updating': False}))

    async def animate_download(self, data: dict):
        """
        下載動漫集數。
        :param data: dict -> 前端傳來要下載動漫的資料。
        :return:
        """
        try:
            if data['episodes']:
                await DB.My.create_log(msg='Myself 下載動漫', action='download')
                try:
                    download_models = await DB.Myself.create_many_download_models(owner_id_list=data['episodes'])
                    download_data_list = await DB.Myself.get_download_animate_episode_data_list(
                        download_models=download_models)
                    myself_download_manage.wait_download_list.extend(download_data_list)
                except Exception as error:
                    print(error)
                # print(animate_episode_list, '123')
                await self.parent.send(
                    text_data=json.dumps({'msg': '下載完成', 'action': data['action'], 'updating': False}))
        except Exception as e:
            print(e)

    async def search_animate(self, data: dict):
        """
        搜尋動漫。
        :param data: dict -> 前端傳來要搜尋動漫的資料。
        :return:
        """
        if data['msg']:
            await DB.My.create_log(msg=f'Myself 搜尋{data["msg"]}動漫', action='search')
            model = await DB.Myself.filter_finish_animate(name__contains=data['msg'])
        else:
            await DB.My.create_log(msg=f'Myself 搜尋動漫', action='search')
            model = await DB.Myself.All_finish_animate()
        serializer_data = await DB.Myself.search_finish_animate_paginator(model=model, page=data.get('page'))
        await self.parent.send(text_data=json.dumps({'data': serializer_data, 'action': data['action']}))

    async def clear_finish_animate(self, data: dict):
        """
        清除已完成下載動漫資料。
        :param data: dict -> 前端傳來要清除已完成下載動漫資料。
        :return:
        """
        await DB.Myself.delete_download_finish_animate()
        await DB.My.create_log(msg='Myself 清除下載已完成', action='delete')
        await myself_download_manage.clear_finish_animate_list()
        await self.parent.send(text_data=json.dumps({'msg': '已清除已完成動漫', 'action': data['action']}))

    async def delete_download_animate(self, data: dict):
        """
        刪除正在下載動漫資料。
        :param data: dict -> 前端傳來要刪除正在下載動漫資料。
        :return:
        """
        DB.Cache.clear_cache()
        await DB.Myself.delete_download_and_ts(download_model__id__in=data['deletes'])
        await DB.My.create_log(msg='Myself 刪除已選取動漫', action='delete')
        await myself_download_manage.delete_download_animate_list(data['deletes'])
        await self.parent.send(text_data=json.dumps({'msg': '已取消勾選的下載動漫', 'action': data['action']}))

    async def download_order(self, data):
        """
        更改動漫下載順序。
        :param data: data: dict -> 前端傳來要更改動漫下載順序。
        :return:
        """
        await myself_download_manage.switch_download_order(data=data)
        await DB.My.create_log(msg='Myself 已更新下載順序', action='switch')
        await self.parent.send(text_data=json.dumps({'msg': '已更新下載順序', 'action': data['action']}))


class Anime1Manage(Base):
    download = anime1_download_manage.download_list
    wait = anime1_download_manage.wait_download_list
    task_action = 'download_anime1_animate_array'

    def __init__(self, parent):
        self.parent = parent

    async def animate_download(self, data: dict):
        """
        下載動漫集數。
        :param data: dict -> 前端傳來要下載動漫的資料。
        :return:
        """
        try:
            if data['episodes']:
                await DB.My.create_log(msg='Anime1 下載動漫', action='download')
                try:
                    ...
                # download_models = await DB.Anime1.create_many_download_models(owner_id_list=data['episodes'])

                except Exception as e:
                    print(e)
                print(data['episodes'])
        except Exception as e:
            print(e)


class AsyncChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Myself = MyselfManage(self)
        self.Anime1 = Anime1Manage(self)

    async def connect(self):
        """
        前端連接。
        :return:
        """
        await self.accept()
        await DB.My.create_log(msg='已連線', action='connect')
        asyncio.create_task(self.Myself.download_tasks())
        asyncio.create_task(self.Anime1.download_tasks())

    async def disconnect(self, close_code):
        """
        前端離開。
        :param close_code:
        :return:
        """
        myself_download_manage.ws = None
        pass

    async def receive(self, text_data: str = None, bytes_data: bytes = None):
        """
        接收前端傳來的值。
        :param text_data: str -> 前端傳來的值。
        :param bytes_data: bytes -> 前端傳來的值。
        :return:
        """

        data = json.loads(text_data)
        print(data)
        try:
            if data.get('action'):
                if data['action'] == 'myself_finish_animate_update':
                    asyncio.create_task(self.Myself.finish_animate_update())
                    await self.send(text_data=json.dumps({'msg': f'正在更新中', 'action': data['action'], 'updating': True}))
                elif data['action'] == 'download_myself_animate':
                    asyncio.create_task(self.Myself.animate_download(data=data))
                    await self.send(
                        text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': data['action'], 'updating': True}))
                elif data['action'] == 'search_myself_animate':
                    asyncio.create_task(self.Myself.search_animate(data=data))
                elif data['action'] == 'clear_finish_myself_animate':
                    asyncio.create_task(self.Myself.clear_finish_animate(data=data))
                elif data['action'] == 'delete_myself_download_animate':
                    asyncio.create_task(self.Myself.delete_download_animate(data=data))
                elif data['action'] == 'download_order_myself_animate':
                    asyncio.create_task(self.Myself.download_order(data=data))
                elif data['action'] == 'download_anime1_animate':
                    asyncio.create_task(self.Anime1.animate_download(data=data))
                elif data['action'] == 'connect':
                    await self.send(text_data=json.dumps({'action': 'connect', 'msg': f'連線成功!!'}))
            # if data.get('msg') and data['msg'] == 'some message to websocket server':
            #     await self.send(text_data=json.dumps({'msg': f'前端在按 Login'}))
            else:
                await self.send(text_data=json.dumps({'msg': f'錯誤的格式', 'action': 'error'}))
        except Exception as error:
            print(error)
            await self.send(text_data=json.dumps({'msg': f'後端出錯了: {error}'}))

# """
# let ws1 = new WebSocket('ws://127.0.0.1:8000/')
# ws1.onmessage = function (e) {
#         const data = JSON.parse(e.data);
#         console.log('ws1', data)
#     };
# ws1.send(JSON.stringify({message: 'hello'}))
# """
