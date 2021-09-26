import asyncio
import json
import random
import time
import threading
from Tools.myself import Myself
from channels.generic.websocket import AsyncWebsocketConsumer


class AsyncChatConsumer(AsyncWebsocketConsumer):
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
        # if data.get('msg'):
        try:
            if data.get('action'):
                if data['action'] == 'myself_finish_animate_update':
                    print('in myself_finish_animate_update')
                    await self.send(text_data=json.dumps({'msg': f'{data["msg"]}'}))
        except Exception  as error:
            print(error)
            await self.send(text_data=json.dumps({'msg': f'後端出錯了: {error}'}))
        # await self.send(text_data=json.dumps({'type': 'click', 'msg': f'我按下去了?: {random.randint(1, 100)}'}))

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
