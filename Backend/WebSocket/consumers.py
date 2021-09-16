import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AsyncChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('hello')
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': ''
        }))


"""
let ws1 = new WebSocket('ws://127.0.0.1:8000/')
ws1.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('ws1', data)
    };
ws1.send(JSON.stringify({message: 'hello'}))
"""
