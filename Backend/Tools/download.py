import asyncio
import json
import threading

from Tools.db import DB
from Tools.myself import Myself


class DownloadManage:
    def __init__(self):
        self.download_list = []
        self.wait_download_list = []
        self.now = 0
        self.max = 2
        self.ws = None
        threading.Thread(target=self.main, args=()).start()

    async def download_ts(self, ts_semaphore, ts_uri, task_data):
        async with ts_semaphore:
            ts_content = await Myself.download_ts_content(ts_uri=ts_uri, host_list=task_data['host_list'],
                                                          video_720p=task_data['video_720p'])
            model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                                   episode_name=task_data['episode_name'])
            await DB.Myself.save_animate_episode_ts_file(uri=ts_uri, parent_model=model,
                                                         ts_content=ts_content)
            task_data['ts_list'].remove(ts_uri)
            task_data['count'] += 1
            # self.download_list[index]['ts_list'].remove(ts_uri)
            # self.download_list[index]['count'] += 1

    async def download_animate(self, task_data: dict):
        ts_semaphore = asyncio.Semaphore(value=10)
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 拿 host')
        animate_video_json, host_list = await Myself.get_animate_video_json_and_host_list(url=task_data['vpx_url'])
        if not task_data.get('ts_list'):
            print(f'{task_data["animate_name"]} {task_data["episode_name"]} 拿 m3u8')
            task_data['ts_list'] = await Myself.get_m3u8_uri_list(host_list=host_list,
                                                                  video_720p=animate_video_json['video']['720p'],
                                                                  timeout=(60, 10))
            task_data['ts_count'] = len(task_data['ts_list'])
            task_data['count'] = 0
            episode_info_model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                                                episode_name=task_data['episode_name'])
            await DB.Myself.create_many_animate_episode_ts(parent_model=episode_info_model,
                                                           ts_list=task_data['ts_list'])

        task_data.update({
            'host_list': sorted(animate_video_json['host'], key=lambda x: x.get('weight'), reverse=True),
            'video_720p': animate_video_json['video']['720p']
        })
        tasks = []
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 開始下載')
        for ts_uri in task_data['ts_list']:
            tasks.append(asyncio.create_task(self.download_ts(ts_semaphore, ts_uri, task_data)))
        await asyncio.gather(*tasks)
        await DB.Myself.save_animate_episode_file(pk=task_data['id'])
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 下載完了')

    async def send_text(self, task_data):
        while True:
            if self.ws:
                try:
                    # index = self.download_list.index(task_data)
                    await self.ws.send(text_data=json.dumps(
                        {'type': 'connect',
                         'msg': f'{task_data["animate_name"]}{task_data["episode_name"]} 已下載了 {task_data["count"] / task_data["ts_count"] * 100}'}))
                except Exception as error:
                    print(error)
            await asyncio.sleep(1)

    async def download_animate_script(self, task_data: dict):
        send = asyncio.create_task(self.send_text(task_data))
        await self.download_animate(task_data=task_data)
        send.cancel()
        await self.ws.send(text_data=json.dumps(
            {'type': 'connect',
             'msg': f'{task_data["animate_name"]}{task_data["episode_name"]} 已下載了 100%'}))
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
                    ts_count = len(ts_list)
                    await DB.Myself.create_many_animate_episode_ts(parent_model=episode_info_model, ts_list=ts_list)
                else:
                    ts_list = await DB.Myself.filter_animate_episode_ts_undone_uri_list(parent_model=episode_info_model)
                    ts_count = await DB.Myself.get_animate_episode_ts_count(parent_model=episode_info_model)

                self.wait_download_list.append({
                    'id': episode_info_model.id,
                    'animate_name': await episode_info_model.get_animate_name(),
                    'episode_name': episode_info_model.name,
                    'vpx_url': new_url,
                    'ts_list': ts_list,
                    'ts_count': ts_count,
                    'count': ts_count - len(ts_list),
                })
        pass

    async def main_task(self):
        await self.get_animate_episode_download_undone_data()
        while True:
            if self.wait_download_list and self.max > self.now:
                self.now += 1
                task_data = self.wait_download_list.pop(0)
                print('開始下載', task_data)
                self.download_list.append(task_data)
                # asyncio.ensure_future(self.download_animate_script(task_data))
                asyncio.create_task(self.download_animate_script(task_data))
            await asyncio.sleep(0.1)

    def main(self):
        asyncio.run(self.main_task())
