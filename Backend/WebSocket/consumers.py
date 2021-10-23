import json
import asyncio

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
        for page in range(total_page_data['total_page'], 0, -1):
            if page == 1:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page),
                                                                  res_text=total_page_data['res_text'])
            else:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page))
            await DB.Myself.create_many_finish_animate(data=page_data)
            # await asyncio.sleep(2)
            if page == 1:
                break
        await create_log(msg='updated', action='myself_finish_animate_update')
        await self.send(
            text_data=json.dumps({'msg': '更新完成', 'action': 'myself_finish_animate_update', 'updating': False}))

    async def myself_animate_download(self, data):
        try:
            if data['episodes']:
                try:
                    animate_episode_list = await DB.Myself.get_many_animate_episode_download_data_and_update_download(
                        pk_list=data['episodes'])
                    download_manage.wait_download_list.extend(animate_episode_list)
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


class AsyncChatConsumer(AsyncWebsocketConsumer, Manage):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'msg': f'連線成功!!'}))
        download_manage.ws = self
        asyncio.create_task(self.download_tasks())

    async def disconnect(self, close_code):
        download_manage.ws = None
        pass

    async def receive(self, text_data=None, bytes_data=None):
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
                    result = await DB.Myself.filter_finish_animate_list(name__contains=data['msg'])
                    print(result)
                    await self.send(text_data=json.dumps({'data': result, 'action': data['action']}))
            if data.get('msg') and data['msg'] == 'some message to websocket server':
                await self.send(text_data=json.dumps({'msg': f'前端在按 Login'}))
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
