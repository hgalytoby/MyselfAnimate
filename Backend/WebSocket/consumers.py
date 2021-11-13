import json
import asyncio

from Api.serializers import FinishAnimateSerializer
from Tools.db import DB
from Tools.download import DownloadManage
from Tools.myself import Myself
from Tools.tools import create_log
from Tools.urls import FinishAnimateUrl, FinishAnimateBaseUrl
from channels.generic.websocket import AsyncWebsocketConsumer

download_manage = DownloadManage()


class Manage:
    async def myself_finish_animate_update(self):
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
        while True:
            # dict(map(lambda kv:: x[''], download_manage.download_list + download_manage.wait_download_list))
            await self.send(
                text_data=json.dumps({
                    'msg': '目前下載列表',
                    'data': download_manage.download_list + download_manage.wait_download_list,
                    'action': 'download_myself_animate_array'}))
            await asyncio.sleep(0.5)

    async def search_animate(self, data: dict):
        if data['msg']:
            model = await DB.Myself.filter_finish_animate(name__contains=data['msg'])
        else:
            model = await DB.Myself.All_finish_animate()
        serializer_data = await DB.Myself.search_finish_animate_paginator(model=model, page=data.get('page'))
        await self.send(text_data=json.dumps({'data': serializer_data, 'action': data['action']}))

    async def clear_finish_animate(self, data: dict):
        await DB.Myself.delete_download_finish_animate()
        download_manage.clear_finish_animate_list()
        await self.send(text_data=json.dumps({'msg': '已清除已完成動漫', 'action': data['action']}))

    async def delete_download_animate(self, data: dict):
        download_manage.delete_download_animate_list(data['deletes'])
        await DB.Myself.delete_download_and_ts(download_model__id__in=data['deletes'])
        await self.send(text_data=json.dumps({'msg': '已取消勾選的下載動漫', 'action': data['action']}))

    async def download_order(self, data):
        download_len = len(download_manage.download_list)
        if data['method'] == 'up' and data['index'] != 0:
            if download_len > data['index']:
                await DB.Myself.switch_download(switch_data1=download_manage.download_list[data['index'] - 1],
                                                switch_data2=download_manage.download_list[data['index']])
                download_manage.download_list[data['index'] - 1], download_manage.download_list[data['index']] = \
                    download_manage.download_list[data['index']], download_manage.download_list[data['index'] - 1]
            else:
                if data['index'] - download_len == 0:
                    await DB.Myself.switch_download(switch_data1=download_manage.wait_download_list[0],
                                                    switch_data2=download_manage.download_list[-1])
                    download_manage.download_list.insert(-1, download_manage.wait_download_list.pop(0))
                else:
                    _ = data['index'] - download_len
                    await DB.Myself.switch_download(switch_data1=download_manage.wait_download_list[_],
                                                    switch_data2=download_manage.wait_download_list[_ - 1])
                    download_manage.wait_download_list[_], download_manage.wait_download_list[_ - 1] = \
                        download_manage.wait_download_list[_ - 1], download_manage.wait_download_list[_]
        elif data['method'] == 'down' and data['index'] != download_len + len(download_manage.wait_download_list) - 1:
            if download_len > data['index'] + 1:
                await DB.Myself.switch_download(switch_data1=download_manage.download_list[data['index']],
                                                switch_data2=download_manage.download_list[data['index'] + 1])
                download_manage.download_list[data['index']], download_manage.download_list[data['index'] + 1] = \
                    download_manage.download_list[data['index'] + 1], download_manage.download_list[data['index']]
            else:
                _ = data['index'] + 1 - download_len
                if data['index'] + 1 - download_len == 0:
                    await DB.Myself.switch_download(switch_data1=download_manage.wait_download_list[0],
                                                    switch_data2=download_manage.download_list[-1])
                    download_manage.download_list.insert(-1, download_manage.wait_download_list.pop(0))
                else:
                    await DB.Myself.switch_download(switch_data1=download_manage.wait_download_list[_ - 1],
                                                    switch_data2=download_manage.wait_download_list[_])
                    download_manage.wait_download_list[_ - 1], download_manage.wait_download_list[_] = \
                        download_manage.wait_download_list[_], download_manage.wait_download_list[_ - 1]
        await self.send(text_data=json.dumps({'msg': '已更新下載順序', 'action': data['action']}))


class AsyncChatConsumer(AsyncWebsocketConsumer, Manage):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'msg': f'連線成功!!'}))
        download_manage.ws = self
        asyncio.create_task(self.download_tasks())

    async def disconnect(self, close_code):
        download_manage.ws = None
        pass

    async def receive(self, text_data: str = None, bytes_data: bytes = None):
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
