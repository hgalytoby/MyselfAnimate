import json
import asyncio

from Tools.db import DB
from Tools.myself import Myself
from Tools.tools import create_log
from Tools.urls import FinishAnimateUrl, FinishAnimateBaseUrl
from channels.generic.websocket import AsyncWebsocketConsumer
import threading


class DownloadManage:
    def __init__(self):
        self.download_list = []
        self.wait_download_list = []
        self.now = 0
        self.max = 2
        threading.Thread(target=self.main, args=()).start()

    @staticmethod
    async def download_ts(ts_semaphore, ts_uri, task_data):
        async with ts_semaphore:
            ts_content = await Myself.download_ts_content(ts_uri=ts_uri, host_list=task_data['host_list'],
                                                          video_720p=task_data['video_720p'])
            model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                                   episode_name=task_data['episode_name'])
            await DB.Myself.save_animate_episode_ts_file(uri=ts_uri, parent_model=model,
                                                         ts_content=ts_content)

    async def download_animate(self, task_data: dict):
        ts_semaphore = asyncio.Semaphore(value=10)
        animate_video_json, host_list = await Myself.get_animate_video_json_and_host_list(url=task_data['vpx_url'])
        if not task_data.get('ts_list'):
            task_data['ts_list'] = await Myself.get_m3u8_uri_list(host_list=host_list,
                                                                  video_720p=animate_video_json['video']['720p'],
                                                                  timeout=(60, 10))
        task_data.update({
            'host_list': sorted(animate_video_json['host'], key=lambda x: x.get('weight'), reverse=True),
            'video_720p': animate_video_json['video']['720p']
        })
        tasks = []
        for ts_uri in task_data['ts_list']:
            tasks.append(asyncio.create_task(self.download_ts(ts_semaphore, ts_uri, task_data)))
        await asyncio.gather(*tasks)
        await DB.Myself.save_animate_episode_file(pk=task_data['id'])
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 下載完了')

    async def download_animate_script(self, task_data: dict):
        await self.download_animate(task_data=task_data)
        self.now -= 1

    async def get_animate_episode_download_undone_data(self):
        animate_dict = {}
        animate_download_undone_list = await DB.Myself.get_animate_episode_download_undone_list()
        for animate in animate_download_undone_list:
            animate_dict.update({animate['name']: await Myself.re_animate_info_video_data(url=animate['url'])})
            for episode_info_model in await DB.Myself.filter_animate_episode_info_downloading_models(
                    owner_id=animate['id']):
                new_url = animate_dict[animate['name']][episode_info_model.name]
                if new_url != episode_info_model.url:
                    await DB.Myself.update_animate_episode_url(new_url=new_url, model=episode_info_model)
                    await DB.Myself.delete_filter_animate_episode_ts(parent_model=episode_info_model)
                    animate_video_json, host_list = await Myself.get_animate_video_json_and_host_list(url=new_url)
                    ts_list = await Myself.get_m3u8_uri_list(host_list=host_list,
                                                             video_720p=animate_video_json['video']['720p'],
                                                             timeout=(60, 10))
                    await DB.Myself.create_many_animate_episode_ts(parent_model=episode_info_model, ts_list=ts_list)
                else:
                    ts_list = await DB.Myself.filter_animate_episode_ts_undone_uri_list(parent_model=episode_info_model)
                self.wait_download_list.append({
                    'id': episode_info_model.id,
                    'animate_name': await episode_info_model.get_animate_name(),
                    'episode_name': episode_info_model.name,
                    'vpx_url': new_url,
                    'ts_list': ts_list,
                })
        pass

    async def main_task(self):
        # await self.get_animate_episode_download_undone_data()
        # print(self.wait_download_list)
        while True:
            print(self.wait_download_list)
            # if self.wait_download_list and self.max > self.now:
            #     self.now += 1
            #     task_data = self.wait_download_list.pop(0)
            #     self.download_list.append(task_data)
            #     asyncio.ensure_future(self.download_animate_script(task_data))
            await asyncio.sleep(1)

    def main(self):
        asyncio.run(self.main_task())


download_manage = DownloadManage()


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

    async def myself_animate_download(self, data):
        try:
            if data['episodes']:
                animate_episode_list = await DB.Myself.get_many_animate_episode_download_data_and_update_download(
                    pk_list=data['episodes'])
                download_manage.wait_download_list.append(animate_episode_list)

                # print(animate_episode_list, '123')
                await self.send(
                    text_data=json.dumps({'msg': '下載完成', 'action': data['action'], 'updating': False}))
        except Exception as e:
            print(e)

    pass


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
                    asyncio.create_task(self.myself_animate_download(data=data))
                    await self.send(
                        text_data=json.dumps({'msg': f'我收到要下載的清單了', 'action': data['action'], 'updating': True}))
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
