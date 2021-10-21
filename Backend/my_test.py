import asyncio
import json
import os
import subprocess
import sys
import threading
import time
import requests
from Tools import setup
from Database.models import AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
#
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from project.settings import MEDIA_PATH

#
#
# async def f(ts_semaphore, index):
#     async with ts_semaphore:
#         print(index)
#         await asyncio.sleep(3)
#
#
# def texst():
#     print('in')
#     time.sleep(1)
#
#
# async def t():
#     tt = threading.Thread(target=texst, args=())
#     tt.start()
#     tt.join()
# try:
cmd = f'ffmpeg -f concat -safe 0 -y -i C:/Python/MyselfAnimate/backend/file.txt -c copy output.mp4'
run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
run.communicate()
run.wait()
# cmd = f'ffmpeg -f concat -safe 0 -y -i {os.getcwd()}/temp/file.txt -c copy {os.getcwd()}/temp/out.mp4'
# # print(cmd)
# print(1)
# proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
#                                              stderr=asyncio.subprocess.PIPE)
# stdout, stderr = await proc.communicate()
# print(2)
# print(os.path.isfile(f'{os.getcwd()}/temp/file.txt'))
# print(stdout, stderr)
# print('1')
# except Exception as e:
#     print(e)


# async def test():
# loop = asyncio.ProactorEventLoop()
# tt = [asyncio.create_task(t())]
# await asyncio.gather(*tt)
# ts_semaphore = asyncio.Semaphore(value=5)
# tasks = []
# for i in range(20):
#     tasks.append(asyncio.create_task(f(ts_semaphore, index=i)))
# await asyncio.gather(*tasks)

# animate = AnimateInfoModel.objects.get(pk=1)
# episode_info = AnimateEpisodeInfoModel.objects.filter(owner=animate).first()
# episode_info = AnimateEpisodeInfoModel.objects.get(id=14)
# print(episode_info.video.url)
# print(episode_info.video)
# print(episode_info.owner.from_website)
# episode_ts = AnimateEpisodeTsModel.objects.filter(owner=episode_info)
# data = []
# for index, ts in enumerate(episode_ts):
#     data.append(f"file '{os.getcwd()}{MEDIA_PATH}/{ts.ts}'")
# with open('file1.txt', 'w', encoding='utf-8') as f:
#     f.write('\n'.join(data))
# loop = asyncio.ProactorEventLoop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(t())
# asyncio.run(t())
# print(os.getcwd())
# cmd = f'ffmpeg -f concat -safe 0 -y -i {os.getcwd()}/temp/file.txt -c copy ./temp/out.mp4'
# run_ffmpeg = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
# run_ffmpeg.wait()
# res = requests.get(url='https://api.github.com/repos/hgalytoby/MyselfAnimeDownloader/traffic/clones', headers={
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
#     'accept': 'application/vnd.github.v3+json',
#     'Authorization': 'Token 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',
# })

# print(res.text)

# print(res.json())

# dd = [{'timestamp': '2021-10-03T00:00:00Z', 'count': 31, 'uniques': 9}]
# data = json.load(open('data.json', 'r', encoding='utf-8'))
#
#
# def get_views():
#     views = requests.get(url='https://api.github.com/repos/hgalytoby/MyselfAnimeDownloader/traffic/views', headers={
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
#         'accept': 'application/vnd.github.v3+json',
#         'Authorization': 'Token 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',
#     }).json()['views']
#     result = list(filter(lambda view: view not in data['views'], views))
#     return result
#
#
# def get_clone():
#     clones = requests.get(url='https://api.github.com/repos/hgalytoby/MyselfAnimeDownloader/traffic/clones', headers={
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
#         'accept': 'application/vnd.github.v3+json',
#         'Authorization': 'Token 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',
#     }).json()['clones']
#     result = list(filter(lambda view: view not in data['clones'], clones))
#     return result


# data['views'].extend(get_views())
# data['clones'].extend(get_clone())
# json.dump(data, open('data.json', 'w', encoding='utf-8'), indent=2)

# if __name__ == '__main__':





image_path = '/x00'
print(len(image_path))
# _split = os.path.split(image_path)
# print(_split)
# _ = list(filter(lambda x: x == _split[1], os.listdir(_split[0])))
# print(_)