import json
import asyncio
from Tools.db import DB
from Tools.myself import Myself
from Tools.download import MyselfDownloadManage, Anime1DownloadManage
from Tools.urls import MyselfFinishAnimateUrl, MyselfFinishAnimateBaseUrl
from channels.generic.websocket import AsyncWebsocketConsumer

from WebSocket.actions import MyselfManage, Anime1Manage

myself_download_manage = MyselfDownloadManage()
anime1_download_manage = Anime1DownloadManage()


class AsyncChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Myself = MyselfManage(parent=self, manage=myself_download_manage)
        self.Anime1 = Anime1Manage(parent=self, manage=anime1_download_manage)
        myself_download_manage.ws.append(self)
        anime1_download_manage.ws.append(self)
        self.action_function = {
            'myself_finish_animate_update': self.Myself.finish_animate_update,
            'download_myself_animate': self.Myself.animate_download,
            'search_myself_animate': self.Myself.search_animate,
            'clear_finish_myself_animate': self.Myself.clear_finish_animate,
            'delete_myself_download_animate': self.Myself.delete_download_animate,
            'download_order_myself_animate': self.Myself.download_order,
            'download_anime1_animate': self.Anime1.animate_download,
            'clear_finish_anime1_animate': self.Anime1.clear_finish_animate,
            'delete_anime1_download_animate': self.Anime1.delete_download_animate,
            'download_order_anime1_animate': self.Anime1.download_order,
            'connect': self.connect_action,
        }

    async def connect_action(self, *args, **kwargs):
        await self.send(text_data=json.dumps({'action': 'connect', 'msg': f'連線成功!!'}))

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
        myself_download_manage.ws.remove(self)
        anime1_download_manage.ws.remove(self)

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
                await self.action_function[data['action']](**data)
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
