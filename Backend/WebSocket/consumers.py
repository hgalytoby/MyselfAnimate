import json
import asyncio
from Tools.db import DB
from Tools.myself import Myself
from Tools.tools import create_log
from Tools.download import DownloadManage
from Tools.urls import FinishAnimateUrl, FinishAnimateBaseUrl
from channels.generic.websocket import AsyncWebsocketConsumer

download_manage = DownloadManage()


class Manage:
    async def myself_finish_animate_update(self):
        """
        更新完結動漫。
        :return:
        """
        total_page_data = await Myself.finish_animate_total_page(url=FinishAnimateUrl, get_res_text=True)
        for page in range(1, total_page_data['total_page'] + 1):
            if page == 1:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page),
                                                                  res_text=total_page_data['res_text'])
            else:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page))
            await DB.Myself.create_many_finish_animate(data=page_data)
        await create_log(msg='updated', action='myself_finish_animate_update')
        await self.send(
            text_data=json.dumps({'msg': '更新完成', 'action': 'myself_finish_animate_update', 'updating': False}))

    async def myself_animate_download(self, data: dict):
        """
        下載動漫集數。
        :param data: dict -> 前端傳來要下載動漫的資料。
        :return:
        """
        try:
            if data['episodes']:
                try:
                    download_models = await DB.Myself.create_many_download_models(owner_id_list=data['episodes'])
                    download_data_list = await DB.Myself.get_download_animate_episode_data_list(
                        download_models=download_models)
                    download_manage.wait_download_list.extend(download_data_list)
                except Exception as error:
                    print(error)
                # print(animate_episode_list, '123')
                await self.send(
                    text_data=json.dumps({'msg': '下載完成', 'action': data['action'], 'updating': False}))
        except Exception as e:
            print(e)

    async def download_tasks(self):
        """
        將現在正要下載的動漫資料傳給前端。
        :return:
        """
        while True:
            # dict(map(lambda kv:: x[''], download_manage.download_list + download_manage.wait_download_list))
            await self.send(
                text_data=json.dumps({
                    'msg': '目前下載列表',
                    'data': download_manage.download_list + download_manage.wait_download_list,
                    'action': 'download_myself_animate_array'}))
            await asyncio.sleep(0.5)

    async def search_animate(self, data: dict):
        """
        搜尋動漫。
        :param data: dict -> 前端傳來要搜尋動漫的資料。
        :return:
        """
        if data['msg']:
            model = await DB.Myself.filter_finish_animate(name__contains=data['msg'])
        else:
            model = await DB.Myself.All_finish_animate()
        serializer_data = await DB.Myself.search_finish_animate_paginator(model=model, page=data.get('page'))
        await self.send(text_data=json.dumps({'data': serializer_data, 'action': data['action']}))

    async def clear_finish_animate(self, data: dict):
        """
        清除已完成下載動漫資料。
        :param data: dict -> 前端傳來要清除已完成下載動漫資料。
        :return:
        """
        await DB.Myself.delete_download_finish_animate()
        download_manage.clear_finish_animate_list()
        await self.send(text_data=json.dumps({'msg': '已清除已完成動漫', 'action': data['action']}))

    async def delete_download_animate(self, data: dict):
        """
        刪除正在下載動漫資料。
        :param data: dict -> 前端傳來要刪除正在下載動漫資料。
        :return:
        """
        download_manage.delete_download_animate_list(data['deletes'])
        await DB.Myself.delete_download_and_ts(download_model__id__in=data['deletes'])
        await self.send(text_data=json.dumps({'msg': '已取消勾選的下載動漫', 'action': data['action']}))

    async def download_order(self, data):
        """
        更改動漫下載順序。
        :param data: data: dict -> 前端傳來要更改動漫下載順序。
        :return:
        """
        await download_manage.switch_download_order(data=data)
        await self.send(text_data=json.dumps({'msg': '已更新下載順序', 'action': data['action']}))


class AsyncChatConsumer(AsyncWebsocketConsumer, Manage):

    async def connect(self):
        """
        前端連接。
        :return:
        """
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'msg': f'連線成功!!'}))
        download_manage.ws = self
        asyncio.create_task(self.download_tasks())

    async def disconnect(self, close_code):
        """
        前端離開。
        :param close_code:
        :return:
        """
        download_manage.ws = None
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
                    asyncio.create_task(self.myself_finish_animate_update())
                    await self.send(text_data=json.dumps({'msg': f'正在更新中', 'action': data['action'], 'updating': True}))
                elif data['action'] == 'download_myself_animate':
                    asyncio.create_task(self.myself_animate_download(data=data))
                    await self.send(
                        text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': data['action'], 'updating': True}))
                elif data['action'] == 'search_myself_animate':
                    asyncio.create_task(self.search_animate(data=data))
                elif data['action'] == 'clear_finish_myself_animate':
                    asyncio.create_task(self.clear_finish_animate(data=data))
                elif data['action'] == 'delete_myself_download_animate':
                    asyncio.create_task(self.delete_download_animate(data=data))
                elif data['action'] == 'download_order_myself_animate':
                    asyncio.create_task(self.download_order(data=data))
            # if data.get('msg') and data['msg'] == 'some message to websocket server':
            #     await self.send(text_data=json.dumps({'msg': f'前端在按 Login'}))
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
