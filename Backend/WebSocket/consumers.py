import asyncio
import json
import random
import time
import threading
from Tools.myself import Myself
from channels.generic.websocket import AsyncWebsocketConsumer

from Tools.urls import FinishAnimateUrl, FinishAnimateBaseUrl


class Manage:
    async def myself_finish_animate_update(self):
        total_page_data = await Myself.finish_animate_total_page(url=FinishAnimateUrl, get_res_text=True)
        for page in range(1, total_page_data['total_page'] + 1):
            if page == 1:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page),
                                                                  res_text=total_page_data['res_text'])
            else:
                page_data = await Myself.finish_animate_page_data(url=FinishAnimateBaseUrl.format(page))
            await Myself.create_finish_animate_data(data=page_data)
            if page == 5:
                break
        await self.send(text_data=json.dumps({'msg': '更新好了'}))


class AsyncChatConsumer(AsyncWebsocketConsumer, Manage):

    async def test2(self):
        week_data = await Myself.week_animate()
        await self.send(text_data=json.dumps({'type': 'while', 'data': week_data}))
        # while True:
        #     await asyncio.sleep(2)
        #     await self.send(text_data=json.dumps({'type': 'while', 'msg': f'一直送: {random.randint(1, 100)}'}))

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'msg': f'連線成功!!'}))
        # asyncio.create_task(self.test2())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)
        try:
            if data.get('action'):
                if data['action'] == 'myself_finish_animate_update':
                    asyncio.create_task(self.test2())
                    await self.myself_finish_animate_update()

        except Exception as error:
            print(error)
            await self.send(text_data=json.dumps({'msg': f'後端出錯了: {error}'}))

    async def test(self):
        _ = random.randint(1, 10)
        await asyncio.sleep(_)
        await self.send(text_data=json.dumps({'msg': f'{_}秒'}))


"""
let ws1 = new WebSocket('ws://127.0.0.1:8000/')
ws1.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('ws1', data)
    };
ws1.send(JSON.stringify({message: 'hello'}))
"""
