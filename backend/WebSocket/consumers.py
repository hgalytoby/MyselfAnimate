import json
import asyncio
import psutil
from Tools.db import DB
from Tools.download import MyselfDownloadManage, Anime1DownloadManage
from channels.generic.websocket import AsyncWebsocketConsumer
from WebSocket.actions import MyselfManage, Anime1Manage

settings = DB.My.get_or_create_settings()
myself_download_manage = MyselfDownloadManage(settings.myself_download_value)
anime1_download_manage = Anime1DownloadManage(settings.anime1_download_value)
ws_array = []


class AsyncChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._storage = {}
        ws_array.append(self)
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
            'update_download_value': self.update_download_value,
            'animate_download_count': self.animate_download_count,
            'update_animate_download_count': self.update_animate_download_count,
            'connect': self.connect_action,
        }

    async def storage(self):
        """
        硬碟空間傳送給前端。
        :return:
        """
        while True:
            _ = psutil.disk_usage('/')
            _storage = {
                # 'total': int(_.total / (2 ** 30)),
                'used': int(_.used / (2 ** 30)),
                'free': int(_.free / (2 ** 30)),
            }
            if self._storage != _storage:
                self._storage = _storage
                await self.send(text_data=json.dumps({
                    'msg': f'硬碟空間',
                    'data': self._storage,
                    'action': 'storage'}))
            await asyncio.sleep(1)

    async def animate_download_count(self, *args, **kwargs):
        """
        全部動漫下載數量送給前端。
        :param args:
        :param kwargs:
        :return:
        """
        myself_count = await DB.Myself.get_animate_download_done_count(done=True)
        anime1_count = await DB.Anime1.get_animate_download_done_count(done=True)
        total = sum([myself_count, anime1_count])
        y_max = 10 if not total else total + max(myself_count, anime1_count)
        await self.send(text_data=json.dumps({
            'msg': f'下載完成數量',
            'data': {
                'values': [myself_count, anime1_count, total],
                'y_max': y_max
            },
            'action': 'downloadCount'}))

    @staticmethod
    async def update_animate_download_count(*args, **kwargs):
        """
        所有 websocket 送全部動漫下載數量訊息給前端。
        :param args:
        :param kwargs:
        :return:
        """
        for ws in ws_array:
            await ws.animate_download_count()

    async def connect_action(self, *args, **kwargs):
        """
        一連線就要做的事情。
        :param args:
        :param kwargs:
        :return:
        """
        await self.send(text_data=json.dumps({'action': 'connect', 'msg': f'連線成功!!'}))
        asyncio.create_task(self.Myself.download_tasks())
        asyncio.create_task(self.Anime1.download_tasks())
        asyncio.create_task(self.storage())
        asyncio.create_task(self.animate_download_count())

    async def update_download_value(self, **kwargs):
        """
        更新動漫同時下載數量。
        :param kwargs:
        :return:
        """
        await self.Myself.manage.update_download_value(value=kwargs['data']['myself_download_value'])
        await self.Anime1.manage.update_download_value(value=kwargs['data']['anime1_download_value'])

    async def connect(self):
        """
        前端連接。
        :return:
        """
        await self.accept()
        await DB.My.async_create_log(msg='已連線', action='connect')

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
