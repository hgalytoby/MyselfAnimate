import asyncio
import json
import random

from Tools.db import DB
from Tools.myself import Myself
from channels.generic.websocket import AsyncWebsocketConsumer

from Tools.tools import create_log, aiohttp_bytes
from Tools.urls import FinishAnimateUrl, FinishAnimateBaseUrl


class Manage:
    async def myself_finish_animate_update(self):
        total_page_data = await Myself.finish_animate_total_page(url=FinishAnimateUrl, get_res_text=True)
        for page in range(1, total_page_data['total_page'] + 1):
            # for page in range(1, 2):
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

    async def myself_animate_info_update(self, data):

        # db_model = await DB.Myself.update_or_create_animate_info(data=data['animateInfo'])
        # await DB.Myself.many_create_animate_episode(data=data, parent_model=db_model)

        await self.send(
            text_data=json.dumps({'msg': '更新完成', 'action': data['action'], 'updating': False}))


class AsyncChatConsumer(AsyncWebsocketConsumer, Manage):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'msg': f'連線成功!!'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)
        try:
            if data.get('action'):
                if data['action'] == 'myself_finish_animate_update':
                    asyncio.create_task(self.myself_finish_animate_update())
                    await self.send(text_data=json.dumps({'msg': f'正在更新中', 'action': data['action'], 'updating': True}))
                elif data['action'] == 'downloadMyselfAnimate':
                    print('in')
                    asyncio.create_task(self.myself_animate_info_update(data=data))
                    await self.send(
                        text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': data['action'], 'updating': True}))
            if data.get('msg') and data['msg'] == 'some message to websocket server':
                await self.send(text_data=json.dumps({'msg': f'前端在按 Login'}))
        except Exception as error:
            print(error)
            await self.send(text_data=json.dumps({'msg': f'後端出錯了: {error}'}))


"""
let ws1 = new WebSocket('ws://127.0.0.1:8000/')
ws1.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('ws1', data)
    };
ws1.send(JSON.stringify({message: 'hello'}))
"""
