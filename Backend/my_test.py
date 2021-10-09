import asyncio

from Tools.db import DB
from Tools.myself import Myself
from Database.models import AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from Tools.tools import aiohttp_text


class DownloadManage:
    def __init__(self):
        self.download_list = []
        self.wait_download_list = []
        self.now = 0
        self.max = 2
        asyncio.run(self.main_task())

    async def download_ts(self, ts_semaphore, ts_uri, task_data):
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
                    'animate_name': await episode_info_model.get_animate_name(),
                    'episode_name': episode_info_model.name,
                    'vpx_url': new_url,
                    'ts_list': ts_list,
                })
        pass

    async def main_task(self):
        await self.get_animate_episode_download_undone_data()
        print(self.wait_download_list)
        while True:
            if self.wait_download_list and self.max > self.now:
                self.now += 1
                task_data = self.wait_download_list.pop(0)
                self.download_list.append(task_data)
                asyncio.ensure_future(self.download_animate(task_data))
            await asyncio.sleep(1)


if __name__ == '__main__':
    DownloadManage()
    pass
