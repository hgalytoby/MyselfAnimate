import asyncio
import io
from contextlib import suppress
import random
import time

from Tools.setup import *
import m3u8
import requests
from django.core.files.base import ContentFile

from Database.models import AnimateEpisodeTsModel
from Tools.db import DB
from bs4 import BeautifulSoup
from Tools.tools import badname, aiohttp_text, aiohttp_json, aiohttp_bytes, SERVER_AND_CLIENT_ERROR

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52',
}
week = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

animate_table = {
    '作品類型': 'animate_type',
    '首播日期': 'premiere_date',
    '播出集數': 'episode',
    '原著作者': 'author',
    '官方網站': 'official_website',
    '備注': 'remarks',
}


class Myself:
    @staticmethod
    def week_animate() -> dict:
        """
        爬首頁的每周更新表。
        :return: dict。
        """
        try:
            # res = requests.get(url='https://myself-bbs.com/portal.php', headers=headers, timeout=(5, 5))
            # if res.ok:
            with open('week.html', 'r', encoding='utf-8') as f:
                res = f.read()
                html = BeautifulSoup(res, features='lxml')
                data = {}
                elements = html.find('div', id='tabSuCvYn')
                for index, elements in enumerate(elements.find_all('div', class_='module cl xl xl1')):
                    animates = []
                    for element in elements:
                        animates.append({
                            'name': element.find('a')['title'],
                            'url': element.find('a')['href'],
                            'update_color': element.find('span').find('font').find('font')['style'],
                            'update': element.find('span').find('font').text,
                        })
                    data.update({week[index]: animates})
                # res.close()
                return data
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    def animate_info(url: str) -> dict:
        """
        取得動漫資料。
        :param url: str -> 要爬的網址。
        :return: dict -> 動漫資料。
        {
            url: 網址,
            video: [{name: 第幾集名稱, url: 網址}]
            name: 名字,
            animate_type: 作品類型,
            premiere_date: 首播日期,
            episode: 播出集數,
            author: 原著作者,
            official_website: 官方網站,
            remarks: 備注,
            synopsis: 簡介
        }
        """
        try:
            res = requests.get(url=url, headers=headers, timeout=(5, 5))
            if res.ok:
                # with open('info.html', 'r', encoding='utf-8') as f:
                #     res_text = f.read()
                html = BeautifulSoup(res.text, features='lxml')
                data = {}
                for elements in html.find_all('div', class_='info_info'):
                    for element in elements.find_all('li'):
                        text = element.text
                        key, value = text.split(': ')
                        data.update({animate_table[key]: value})
                    for element in elements.find_all('p'):
                        data.update({'synopsis': element.text})
                for elements in html.find_all('div', class_='info_img_box fl'):
                    for element in elements.find_all('img'):
                        data.update({'image': element['src']})
                videos = []
                for main_list in html.select('ul.main_list'):
                    for a in main_list.find_all('a', href='javascript:;'):
                        name = a.text
                        for display in a.parent.select("ul.display_none li"):
                            if display.select_one("a").text == '站內':
                                a = display.select_one("a[data-href*='v.myself-bbs.com']")
                                video_url = a["data-href"].replace('player/play', 'vpx').replace("\r", "").replace("\n",
                                                                                                                   "")
                                videos.append({'name': badname(name=name), 'url': video_url})
                data.update({'url': url, 'name': badname(html.find('title').text.split('【')[0]), 'video': videos})
                res.close()
                return data
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    def finish_list() -> dict:
        """
        爬完結列表頁面的動漫資訊
        :return: dict。
        """
        # url = 'https://myself-bbs.com/portal.php?mod=topic&topicid=8'
        # res = requests.get(url=url, headers=headers)
        with open('finish_list.html', 'r', encoding='utf-8') as f:
            res = f.read()
        # html = BeautifulSoup(res.text, features='lxml')
        html = BeautifulSoup(res, features='lxml')
        data = []
        for elements in html.find_all('div', {'class': 'tab-title title column cl'}):
            year_list = []
            for element in elements.find_all('div', {'class': 'block move-span'}):
                year_month_title = element.find('span', {'class': 'titletext'}).text
                season_list = []
                for k in element.find_all('a'):
                    season_list.append({'name': k['title'], 'url': f"https://myself-bbs.com/{k['href']}"})
                year_list.append({'title': year_month_title, 'data': season_list})
            data.append({'data': year_list})
        # res.close()
        return {'data': data}

    @staticmethod
    async def get_vpx_json(url: str, timeout: tuple = (10, 10)) -> dict:
        """
        :param url:
        :param timeout:
        :return:
        """
        return await aiohttp_json(url=url, timeout=timeout)

    @staticmethod
    async def get_m3u8_data(host_list: list, video_720p=str, timeout: tuple = (10, 10)) -> object:
        """

        :param host_list:
        :param timeout:
        :return:
        """
        s1 = time.time()
        change = 0
        host_list_len = len(host_list)
        while True:
            m3u8_url = f"{host_list[change]['host']}{video_720p}"
            try:
                res_text = await aiohttp_text(url=m3u8_url, timeout=timeout)
                break
            except SERVER_AND_CLIENT_ERROR:
                if change > host_list_len - 1:
                    change = 0
                else:
                    change += 1
                print('ServerClientConnectionError')
            await asyncio.sleep(1)
        print(time.time() - s1)
        try:
            return m3u8.loads(res_text)
        except BaseException as error:
            print(f'get_m3u8 error: {error}')
            return None

    @staticmethod
    async def finish_animate_total_page(url, get_res_text=False) -> dict:
        """
        爬完結動漫總頁數多少。
        :param url: str -> 要爬的網址。
        :param get_res_text: bool -> True = 將 requests.text 返回。
        :return: dict -> 該頁的資料。
        {
            total_page: 總頁數,
            html: 該頁面的資料。
        }
        """
        res_text = await aiohttp_text(url=url)
        html = BeautifulSoup(res_text, 'lxml')
        page_data = html.find('div', class_='pg').find('a', class_='last').text
        if page_data and get_res_text:
            return {'total_page': int(page_data.replace('... ', '')), 'res_text': res_text}
        else:
            return {'total_page': int(page_data.replace('... ', ''))}

    @staticmethod
    async def finish_animate_page_data(url, res_text=None) -> list:
        """
        完結動漫頁面的動漫資料。
        :param url: str -> 要爬的網址。
        :param res_text: str -> 給完結動漫某頁的HTML，就不用在 requests 了。
        :return: list -> 該頁的資料。
        """
        if not res_text:
            res_text = await aiohttp_text(url=url)
        html = BeautifulSoup(res_text, 'lxml')
        data = []
        for elements in html.find_all('div', class_='c cl'):
            data.append({
                'url': f"https://myself-bbs.com/{elements.find('a')['href']}",
                'name': badname(elements.find('a')['title']),
                'image': f"https://myself-bbs.com/{elements.find('a').find('img')['src']}"
            })
        return data

    @classmethod
    async def many_start_download_animate(cls, models, animate_name):
        for model in models:
            animate_video_json = await cls.get_vpx_json(model.url, timeout=(60, 10))
            host_list = sorted(animate_video_json['host'], key=lambda x: x.get('weight'), reverse=True)
            # m3u8_url = f"{host_list[0]['host']}{animate_video_json['video']['720p']}"
            m3u8_obj = await cls.get_m3u8_data(host_list=host_list, video_720p=animate_video_json['video']['720p'],
                                               timeout=(60, 10))
            try:
                if await DB.Myself.get_animate_episode_ts_count(parent_model=model) != len(m3u8_obj.segments):
                    await DB.Myself.delete_filter_animate_episode_ts(parent_model=model)
                    await DB.Myself.many_create_animate_episode_ts(parent_model=model, m3u8_obj=m3u8_obj)
                else:
                    print('else')
                for obj in m3u8_obj.segments:
                    ts_content = await cls.download_ts_content(uri=obj.uri, host_list=host_list,
                                                               video_720p=animate_video_json['video']['720p'])
                    await DB.Myself.save_animate_episode_ts_file(uri=obj.uri, parent_model=model, ts_content=ts_content)
            except Exception as e:
                print(e)

    @classmethod
    async def download_ts_content(cls, uri: str, host_list: list, video_720p: str):
        change = 0
        host_list_len = len(host_list)
        while True:
            ts_url = f"{host_list[0]['host']}{video_720p.replace('720p.m3u8', uri)}"
            try:
                return await aiohttp_bytes(url=ts_url, timeout=(30, 10))
            except SERVER_AND_CLIENT_ERROR:
                if change > host_list_len - 1:
                    change = 0
                else:
                    change += 1
                print('ServerClientConnectionError')
            await asyncio.sleep(1)


async def main():
    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
    #     async with session.get(url='https://vpx06.myself-bbs.com/47690/003/720p.m3u8', headers=headers) as res:
    #         print(await res.text(encoding='utf-8', errors='ignore'))
    # _ = await Myself.finish_animate_page_data(url='https://myself-bbs.com/forum-113-1.html')
    # await DB.Myself.create_many_finish_animate(_)
    # a = await Myself.get_m3u8_data(url='https://vpx.myself-bbs.com/47731/012/720p.m3u8')
    pass


class Test:
    def __init__(self):
        self.count = 0
        self.now = 0
        self.max = 2
        self.mission = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    async def ts_test(self, ts_semaphore, i, c):
        async with ts_semaphore:
            r = random.randint(1, 5)
            await asyncio.sleep(r)
            return i, r

    async def read(self):
        ts_semaphore = asyncio.Semaphore(value=5)
        c = self.count
        tasks = []
        for i in range(10):
            tasks.append(asyncio.create_task(self.ts_test(ts_semaphore, i, c)))
        await asyncio.gather(*tasks)
        self.now -= 1

    async def main_task(self):
        while True:
            if self.mission and self.max > self.now:
                self.now += 1
                self.count += 1
                self.mission.pop(0)
                asyncio.ensure_future(self.read())
                print(self.count)
            await asyncio.sleep(1)

    def main_test(self):
        asyncio.run(self.main_task())


if __name__ == '__main__':
    # asyncio.run(main())
    t = Test()
    t.main_test()
    pass
