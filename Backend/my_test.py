import asyncio
import os
import subprocess
import sys
import threading
import time

from Tools import setup
from Database.models import AnimateInfoModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
#
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
# cmd = f'ffmpeg -f concat -safe 0 -y -i {os.getcwd()}/temp/file.txt -c copy {os.getcwd()}/temp/out.mp4'
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
episode_info = AnimateEpisodeInfoModel.objects.get(id=14)
print(episode_info.video.url)
print(episode_info.video)
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

