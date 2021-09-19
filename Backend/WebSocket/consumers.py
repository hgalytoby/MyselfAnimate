import asyncio
import json
import random
import time
import threading
from Tools.MyselfTool import Myself
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
        # asyncio.create_task(self.test2())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)

        await self.send(text_data=json.dumps({'type': 'click', 'msg': f'我按下去了?: {random.randint(1, 100)}'}))


"""
let ws1 = new WebSocket('ws://127.0.0.1:8000/')
ws1.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('ws1', data)
    };
ws1.send(JSON.stringify({message: 'hello'}))
"""
