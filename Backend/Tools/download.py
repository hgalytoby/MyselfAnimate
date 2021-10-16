import asyncio
import json
import subprocess
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

    @staticmethod
    async def download_ts(ts_semaphore, ts_uri, task_data):
        async with ts_semaphore:
            ts_content = await Myself.download_ts_content(ts_uri=ts_uri, host_list=task_data['host_list'],
                                                          video_720p=task_data['video_720p'])
            model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                                   episode_name=task_data['episode_name'])
            await DB.Myself.save_animate_episode_ts_file(uri=ts_uri, parent_model=model,
                                                         ts_content=ts_content)
            task_data['ts_list'].remove(ts_uri)
            task_data['count'] += 1

    async def _process_host(self, task_data):
        await self.ws_send_msg(msg={
            'type': 'download',
            'status': '取得 Host 資料中',
            'name': f'{task_data["animate_name"]} {task_data["episode_name"]}',
            'progress_rate': 0
        })
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 拿 host')
        animate_video_json, host_list = await Myself.get_animate_video_json_and_host_list(url=task_data['vpx_url'])
        task_data.update({
            'host_list': sorted(animate_video_json['host'], key=lambda x: x.get('weight'), reverse=True),
            'video_720p': animate_video_json['video']['720p'],
        })
        return animate_video_json, host_list

    async def _process_m3u8(self, animate_video_json, host_list, task_data):
        await self.ws_send_msg(msg={
            'type': 'download',
            'status': '取得 M3U8 資料中',
            'name': f'{task_data["animate_name"]} {task_data["episode_name"]}',
            'progress_rate': 0
        })
        episode_info_model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                                            episode_name=task_data['episode_name'])
        task_data['ts_list'] = await Myself.get_m3u8_uri_list(host_list=host_list, timeout=(60, 10),
                                                              video_720p=animate_video_json['video']['720p'])
        task_data.update({'ts_count': len(task_data['ts_list'])})
        await DB.Myself.create_many_animate_episode_ts(parent_model=episode_info_model, ts_list=task_data['ts_list'])

    async def _process_merge_video(self, task_data):
        await self.ws_send_msg(msg={
            'type': 'download',
            'status': '合併影片中',
            'name': f'{task_data["animate_name"]} {task_data["episode_name"]}',
            'progress_rate': 100
        })
        model = await DB.Myself.get_animate_episode_info_model(animate_name=task_data['animate_name'],
                                                               episode_name=task_data['episode_name'])
        ts_path_list = await DB.Myself.filter_animate_episode_ts_undone_ts_list(parent_model=model)
        with open(f'./temp/{task_data["animate_name"]} {task_data["episode_name"]}.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(ts_path_list))
        cmd = f'ffmpeg -f concat -safe 0 -y -i ./temp/{task_data["animate_name"]} {task_data["episode_name"]}.txt -c ./temp/{task_data["animate_name"]} {task_data["episode_name"]}.mp4'
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        run.wait()
        with open(f'./temp/{task_data["animate_name"]} {task_data["episode_name"]}.mp4', 'rb') as f:
            await DB.Myself.save_animate_episode_video_file(name=task_data["episode_name"], parent_model=model,
                                                            video_content=f.read())
        await self.ws_send_msg(msg={
            'type': 'download',
            'status': '下載完成',
            'name': f'{task_data["animate_name"]} {task_data["episode_name"]}',
            'progress_rate': 100
        })

    async def download_animate(self, task_data: dict):
        ts_semaphore = asyncio.Semaphore(value=10)
        animate_video_json, host_list = await self._process_host(task_data=task_data)
        if not task_data.get('ts_list'):
            print(f'{task_data["animate_name"]} {task_data["episode_name"]} 拿 m3u8')
            await self._process_m3u8(animate_video_json=animate_video_json, host_list=host_list, task_data=task_data)
        tasks = []
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 開始下載')
        for ts_uri in task_data['ts_list']:
            tasks.append(asyncio.create_task(self.download_ts(ts_semaphore, ts_uri, task_data)))
        send_download_msg = asyncio.create_task(self.send_download_msg(task_data=task_data))
        await asyncio.gather(*tasks)
        await DB.Myself.save_animate_episode_file(pk=task_data['id'])
        send_download_msg.cancel()
        await self._process_merge_video(task_data=task_data)
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 下載完了')
        # self.now -= 1

    async def ws_send_msg(self, msg):
        if self.ws:
            try:
                await self.ws.send(text_data=json.dumps(msg))
            except Exception as error:
                print(error)

    async def send_download_msg(self, task_data):
        name = f'{task_data["animate_name"]}{task_data["episode_name"]}'
        while True:
            await self.ws_send_msg(msg={
                'type': 'download',
                'status': '下載中',
                'name': name,
                'progress_rate': f'{task_data["count"] / task_data["ts_count"] * 100}'
            })
            await asyncio.sleep(1)

    async def download_animate_script(self, task_data: dict):
        await self.download_animate(task_data=task_data)
        # await self.ws.send(text_data=json.dumps(
        #     {'type': 'connect',
        #      'msg': f'{task_data["animate_name"]}{task_data["episode_name"]} 已下載了 100%'}))
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
                asyncio.create_task(self.download_animate_script(task_data))
            await asyncio.sleep(0.1)

    def main(self):
        asyncio.run(self.main_task())
