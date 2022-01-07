import asyncio
import json
import os
import shutil
import threading
import subprocess

import aiohttp

from Tools.anime1 import Anime1
from Tools.db import DB
from Tools.myself import Myself
from project.settings import MEDIA_PATH, ROOT_MEDIA_PATH


class BaseDownloadManage:
    def __init__(self):
        self.download_list = []
        self.wait_download_list = []
        self.connections = 10
        self.tasks_dict = {}
        self.now = 0
        self.max = 2
        self.ws = []
        self.switch_db_function = NotImplemented

    async def clear_finish_animate_list(self):
        """
        清除陣列已完成的動漫。
        :return:
        """
        self.download_list = list(filter(lambda x: not x['done'], self.download_list))
        self.wait_download_list = list(filter(lambda x: not x['done'], self.wait_download_list))

    async def delete_download_animate_list(self, deletes: list):
        """
        刪除陣列中的動漫。
        :param deletes:
        :return:
        """
        self.wait_download_list = list(filter(lambda x: x['id'] not in deletes, self.wait_download_list))
        # self.tasks_dict[x['id']].cancel() 這個方法是要取消 async 的任務，如果成功取消會回傳 True。
        # 因為回傳 True 導致這個 filter 判斷明明進入到 else 卻因為拿到 True 然後跳回 if 成立接著將 x 回傳出去。
        # 所以要用 not self.tasks_dict[x['id']]，才能防止不回傳值時會回傳值的問題。
        self.download_list = list(
            filter(lambda x: x if x['id'] not in deletes else False if x['done'] else not self.tasks_dict[
                x['id']].cancel(), self.download_list))
        # 下面的 for 就是上面 filter 在做的事情。
        # for item in self.download_list:
        #     if item['id'] in deletes:
        #         if not item['done']:
        #             self.tasks_dict[item['id']].cancel()
        #         self.download_list.remove(item)

    async def switch_download_order(self, data: dict):
        """
        交換下載順序。
        :param data: dict -> 動漫集數的資料。
        :return:
        """
        download_len = len(self.download_list)
        if data['method'] == 'up' and data['index'] != 0:
            if download_len > data['index']:
                await self.switch_db_function(switch_data1=self.download_list[data['index'] - 1],
                                              switch_data2=self.download_list[data['index']])
                self.download_list[data['index'] - 1], self.download_list[data['index']] = \
                    self.download_list[data['index']], self.download_list[data['index'] - 1]
            else:
                if data['index'] - download_len == 0:
                    await self.switch_db_function(switch_data1=self.wait_download_list[0],
                                                  switch_data2=self.download_list[-1])
                    self.download_list.insert(-1, self.wait_download_list.pop(0))
                else:
                    _ = data['index'] - download_len
                    await self.switch_db_function(switch_data1=self.wait_download_list[_],
                                                  switch_data2=self.wait_download_list[_ - 1])
                    self.wait_download_list[_], self.wait_download_list[_ - 1] = \
                        self.wait_download_list[_ - 1], self.wait_download_list[_]
        elif data['method'] == 'down' and data['index'] != download_len + len(self.wait_download_list) - 1:
            if download_len > data['index'] + 1:
                await self.switch_db_function(switch_data1=self.download_list[data['index']],
                                              switch_data2=self.download_list[data['index'] + 1])
                self.download_list[data['index']], self.download_list[data['index'] + 1] = \
                    self.download_list[data['index'] + 1], self.download_list[data['index']]
            else:
                _ = data['index'] + 1 - download_len
                if data['index'] + 1 - download_len == 0:
                    await self.switch_db_function(switch_data1=self.wait_download_list[0],
                                                  switch_data2=self.download_list[-1])
                    self.download_list.insert(-1, self.wait_download_list.pop(0))
                else:
                    await self.switch_db_function(switch_data1=self.wait_download_list[_ - 1],
                                                  switch_data2=self.wait_download_list[_])
                    self.wait_download_list[_ - 1], self.wait_download_list[_] = \
                        self.wait_download_list[_], self.wait_download_list[_ - 1]

    async def main_task(self):
        while True:
            if self.wait_download_list and self.max > self.now:
                self.now += 1
                task_data = self.wait_download_list.pop(0)
                print('開始下載', task_data['animate_name'], task_data['episode_name'], task_data['id'])
                self.download_list.append(task_data)
                self.tasks_dict.update({task_data['id']: asyncio.create_task(self.download_animate_script(task_data))})
                pass
            await asyncio.sleep(0.1)

    async def animate_finish_send_ws(self, task_data):
        for ws in self.ws:
            await ws.send(text_data=json.dumps({
                'msg': f'下載完成',
                'data': {
                    'animate_name': task_data['animate_name'],
                    'episode_name': task_data['episode_name'],
                },
                'action': 'download_animate_finish'}))


class MyselfDownloadManage(BaseDownloadManage):
    def __init__(self):
        super(MyselfDownloadManage, self).__init__()
        self.from_website = 'Myself'
        self.switch_db_function = DB.Myself.switch_download
        threading.Thread(target=self.main, args=()).start()

    @staticmethod
    async def download_ts(ts_semaphore: asyncio.Semaphore, ts_uri: str, task_data: dict):
        """
        下載 ts 檔案。
        :param ts_semaphore: asyncio.Semaphore -> 最大同時數量。
        :param ts_uri: str -> ts url。
        :param task_data: dict -> 動漫集數的資料。
        :return:
        """
        try:
            async with ts_semaphore:
                ts_content = await Myself.download_ts_content(ts_uri=ts_uri, host_list=task_data['host_list'],
                                                              video_720p=task_data['video_720p'])
                model = await DB.Myself.get_animate_episode_info_model(owner__name=task_data['animate_name'],
                                                                       name=task_data['episode_name'])
                await DB.Myself.save_animate_episode_ts_file(uri=ts_uri, owner=model, ts_content=ts_content)
                task_data['ts_list'].remove(ts_uri)
                task_data['count'] += 1
        except Exception as error:
            print(error, 'download_ts')
            pass

    @staticmethod
    def __process_merge_video(cmd: str):
        """
        以下這三行程式碼是在 Windows 上需要這麼做，但是會報 Cannot run the event loop while another loop is running 錯誤訊息。
        我用一般 py 寫一個測試時可以這樣使用，但是在 Django 裡會不行。
        也有找過
        import nest_asyncio
        nest_asyncio.apply()
        依然不行，暫時無解。
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__process_merge_video(cmd=cmd))
        :param cmd: str - ffmpeg 合併的指令。
        :return:
        """
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        run.communicate()
        run.wait()
        # proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
        #                                              stderr=asyncio.subprocess.PIPE)
        # _, _ = await proc.communicate()

    @staticmethod
    async def _process_host(task_data: dict) -> bool:
        """
        取得動漫集數的 host 資料。
        :param task_data: dict -> 動漫集數的資料。
        :return: bool
        """
        task_data.update({'status': '取得 Host 資料中'})
        print(f"{task_data['animate_name']} {task_data['episode_name']} 拿 host")
        animate_video_json = await Myself.get_animate_video_json(url=task_data['vpx_url'])
        if not animate_video_json:
            task_data.update({'status': '官網更新資料!請刪除後重新下載!'})
            return False
        task_data.update({
            'animate_video_json': animate_video_json,
            'host_list': sorted(animate_video_json['host'], key=lambda x: x.get('weight'), reverse=True),
            'video_720p': animate_video_json['video']['720p'],
        })
        return True

    @staticmethod
    async def _process_m3u8(task_data: dict) -> bool:
        """
        取得動漫集數的 m3u8 資料。
        :param task_data: dict -> 動漫集數的資料。
        :return: bool
        """
        task_data.update({'status': '取得 M3U8 資料中'})
        episode_info_model = await DB.Myself.get_animate_episode_info_model(owner__name=task_data['animate_name'],
                                                                            name=task_data['episode_name'])
        ts_list = await Myself.get_m3u8_uri_list(host_list=task_data['host_list'], timeout=(60, 10),
                                                 video_720p=task_data['animate_video_json']['video']['720p'])
        if not ts_list:
            task_data.update({'status': '官網更新資料!請刪除後重新下載!'})
            return False
        task_data['ts_list'] = ts_list
        task_data.update({'ts_count': len(task_data['ts_list'])})
        await DB.Myself.create_many_animate_episode_ts(owner=episode_info_model, ts_list=task_data['ts_list'])
        return True

    async def _process_merge_video(self, task_data: dict):
        """
        將 ts 影片合併成 mp4。
        :param task_data:  dict -> 動漫集數的資料。
        :return:
        """
        task_data.update({'status': '合併影片中'})
        try:
            model = await DB.Myself.get_animate_episode_info_model(owner__name=task_data['animate_name'],
                                                                   name=task_data['episode_name'])
            ts_list_path = f'{self.from_website}/{task_data["animate_name"]}/video/ts/{task_data["episode_name"]}/ts_list.txt'
            video_path = f'{self.from_website}/{task_data["animate_name"]}/video/{task_data["episode_name"]}.mp4'
            ts_path_list = await DB.Myself.filter_animate_episode_ts_list(owner=model)
            with open(f'{ROOT_MEDIA_PATH}{ts_list_path}', 'w', encoding='utf-8') as f:
                f.write('\n'.join(ts_path_list))
            cmd = f'ffmpeg -f concat -safe 0 -y -i "{ROOT_MEDIA_PATH}{ts_list_path}" -c copy "{ROOT_MEDIA_PATH}{video_path}"'
            _ = threading.Thread(target=self.__process_merge_video, args=(cmd,))
            _.start()
            _.join()
            await DB.Myself.save_animate_episode_video_file(pk=task_data['episode_id'], video_path=video_path)
            await DB.Myself.delete_filter_animate_episode_ts(owner_id=task_data['episode_id'])
            task_data['video'] = f'{MEDIA_PATH}/{video_path}'
            task_data['done'] = True
        except Exception as error:
            print(error, '_process_merge_video')

    async def download_animate(self, task_data: dict):
        """
        開始下載動漫集數。
        :param task_data: 動漫集數的資料。
        :return:
        """
        ts_semaphore = asyncio.Semaphore(value=self.connections)
        if not await self._process_host(task_data=task_data):
            return
        if not task_data.get('ts_list'):
            print(f'{task_data["animate_name"]} {task_data["episode_name"]} 拿 m3u8')
            if not await self._process_m3u8(task_data=task_data):
                return
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 開始下載')
        task_data.update({'status': '下載中'})
        tasks = []
        for ts_uri in task_data['ts_list']:
            tasks.append(asyncio.create_task(self.download_ts(ts_semaphore, ts_uri, task_data)))
        await asyncio.gather(*tasks)
        print(f'{task_data["animate_name"]} {task_data["episode_name"]} 下載完了')

    async def download_animate_script(self, task_data: dict):
        """
        下載動漫腳本。
        :param task_data: 動漫集數的資料。
        :return:
        """
        try:
            if not task_data['done']:
                await self.download_animate(task_data=task_data)
        except asyncio.CancelledError:
            print(f'取消下載: {task_data["animate_name"]} {task_data["episode_name"]}')
        else:
            print('else try')
            if not task_data['video']:
                await self._process_merge_video(task_data=task_data)
                await DB.My.create_history(animate_website_name=self.from_website,
                                           animate_name=task_data['animate_name'],
                                           episode_name=task_data['episode_name'])
                await self.animate_finish_send_ws(task_data=task_data)
            task_data.update({'status': '下載完成'})
        self.now -= 1

    async def main_task(self):
        """
        主要方法。
        :return:
        """
        download_models = await DB.Myself.get_total_download_animate_episode_models()
        self.wait_download_list += await DB.Myself.get_download_animate_episode_data_list(
            download_models=download_models)
        await super(MyselfDownloadManage, self).main_task()

    def main(self):
        """
        開始異步執行。
        :return:
        """
        asyncio.run(self.main_task())


class Anime1DownloadManage(BaseDownloadManage):
    def __init__(self):
        super(Anime1DownloadManage, self).__init__()
        self.from_website = 'Anime1'
        self.switch_db_function = DB.Anime1.switch_download
        threading.Thread(target=self.main, args=()).start()

    async def download_animate(self, task_data, animate_url, cookies):
        _headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'cookie': cookies
        }
        _timeout = aiohttp.client.ClientTimeout(sock_connect=10, sock_read=10)
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
                async with session.get(url=animate_url, headers=_headers, timeout=_timeout) as res:
                    task_data.update({'status': '下載中'})
                    # video_path = f'{self.from_website}/{task_data["animate_name"]}/'
                    animate_dir_path = f'{MEDIA_PATH}/{self.from_website}/{task_data["animate_name"]}/'
                    if not os.path.isdir(f'.{animate_dir_path}'):
                        os.makedirs(f'.{animate_dir_path}')
                    save_path = f'{self.from_website}/{task_data["animate_name"]}/{task_data["episode_name"]}.mp4'
                    video_path = f'{MEDIA_PATH}/{save_path}'
                    with open(f'.{video_path}', 'wb') as fd:
                        download_content_length = 0
                        while True:
                            chunk = await res.content.read(1024 * 10)
                            download_content_length += len(chunk)
                            if not chunk:
                                break
                            fd.write(chunk)
                            task_data['progress_value'] = int(download_content_length / res.content_length * 100)
                        await DB.Anime1.save_animate_episode_video_file(pk=task_data['episode_id'],
                                                                        video_path=save_path)
                        task_data['video'] = video_path
                        task_data['done'] = True
        except Exception as e:
            print(e)

    async def download_animate_script(self, task_data):
        try:
            if task_data['done']:
                task_data['progress_value'] = 100
            else:
                api_key, api_value = await Anime1.get_api_key_and_value(url=task_data['url'])
                animate_url, cookies = await Anime1.get_cookies_and_animate_url(api_key=api_key, api_value=api_value)
                await self.download_animate(task_data, animate_url, cookies)
                await DB.My.create_history(animate_website_name=self.from_website,
                                           animate_name=task_data["animate_name"],
                                           episode_name=task_data["episode_name"])
                await self.animate_finish_send_ws(task_data=task_data)
        except asyncio.CancelledError:
            print(f'取消下載: {task_data["name"]}')
        else:
            task_data.update({'status': '下載完成'})
        self.now -= 1

    async def main_task(self):
        download_models = await DB.Anime1.get_total_download_animate_episode_models()
        self.wait_download_list += await DB.Anime1.get_download_animate_episode_data_list(
            download_models=download_models)
        await super(Anime1DownloadManage, self).main_task()

    def main(self):
        """
        開始異步執行。
        :return:
        """
        asyncio.run(self.main_task())
