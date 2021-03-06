import asyncio
import json
import time
import m3u8
import requests

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
# week = {
#     0: '星期一',
#     1: '星期二',
#     2: '星期三',
#     3: '星期四',
#     4: '星期五',
#     5: '星期六',
#     6: '星期日',
# }

animate_table = {
    '作品類型': 'animate_type',
    '首播日期': 'premiere_date',
    '播出集數': 'episode',
    '原著作者': 'author',
    '官方網站': 'official_website',
    '備注': 'remarks',
    '簡介': 'synopsis',
}


class Myself:
    @staticmethod
    def week_animate() -> dict:
        """
        爬首頁的每周更新表。
        :return: dict。
        """
        try:
            res = requests.get(url='https://myself-bbs.com/portal.php', headers=headers, timeout=(5, 5))
            if res.ok:
                html = BeautifulSoup(res.text, features='lxml')
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
                res.close()
                return data
        except requests.exceptions.RequestException as error:
            print(f'week_animate: {error}')
            return {}

    @staticmethod
    def animate_info_video_data(html: BeautifulSoup) -> list:
        """
        取得影片 Api Host Url。
        :param html:
        :return:
        """
        data = []
        for main_list in html.select('ul.main_list'):
            for a in main_list.find_all('a', href='javascript:;'):
                name = a.text
                for display in a.parent.select("ul.display_none li"):
                    if display.select_one("a").text == '站內':
                        a = display.select_one("a[data-href*='v.myself-bbs.com']")
                        video_url = a["data-href"].replace('player/play', 'vpx').replace("\r", "").replace("\n", "")
                        data.append({'name': badname(name=name), 'url': video_url})
        return data

    @staticmethod
    async def re_animate_info_video_data(url: str) -> dict:
        res_text = await aiohttp_text(url=url)
        html = BeautifulSoup(res_text, 'lxml')
        video_data = Myself.animate_info_video_data(html=html)
        return dict(map(lambda kv: (kv['name'], kv['url']), video_data))

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
                video = Myself.animate_info_video_data(html=html)
                data.update({'url': url, 'name': badname(html.find('title').text.split('【')[0]), 'video': video})
                res.close()
                return data
        except requests.exceptions.RequestException as error:
            print(f'animate_info_error: {error}')
            return {}

    @staticmethod
    def finish_list() -> list:
        """
        爬完結列表頁面的動漫資訊
        :return: dict。
        """
        try:
            url = 'https://myself-bbs.com/portal.php?mod=topic&topicid=8'
            res = requests.get(url=url, headers=headers)
            html = BeautifulSoup(res.text, features='lxml')
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
            res.close()
            return data
        except requests.exceptions.RequestException as error:
            print(f'finish_list: {error}')
            return []

    @staticmethod
    async def get_vpx_json(url: str, timeout: tuple = (10, 10)) -> dict:
        """
        :param url:
        :param timeout:
        :return:
        """
        error_count = 0
        while True:
            try:
                return await aiohttp_json(url, timeout=timeout)
            except SERVER_AND_CLIENT_ERROR:
                if error_count == 20:
                    return {}
                error_count += 1
                print('ServerClientConnectionError')
            await asyncio.sleep(3)

    @staticmethod
    async def get_m3u8_uri_list(host_list: list, video_720p=str, timeout: tuple = (10, 10)) -> list:
        """
        :param host_list:
        :param video_720p:
        :param timeout:
        :return:
        """
        s1 = time.time()
        change = 0
        error_count = 0
        host_list_len = len(host_list)
        while True:
            m3u8_url = f"{host_list[change]['host']}{video_720p}"
            try:
                res_text = await aiohttp_text(url=m3u8_url, timeout=timeout)
                break
            except SERVER_AND_CLIENT_ERROR:
                if error_count == 20:
                    return []
                error_count += 1
                if change > host_list_len - 1:
                    change = 0
                else:
                    change += 1
                print('ServerClientConnectionError')
            await asyncio.sleep(1)
        print(time.time() - s1)
        try:
            m3u8_obj = m3u8.loads(res_text)
            ts_list = []
            for m3u8_obj in m3u8_obj.segments:
                ts_list.append(m3u8_obj.uri)
            return ts_list
        except BaseException as error:
            print(f'get_m3u8 error: {error}')
            return []

    @staticmethod
    async def finish_animate_total_page(url: str, get_res_text: bool = False) -> dict:
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
    async def finish_animate_page_data(url: str, res_text: str = None) -> list:
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
                'image': f"https://myself-bbs.com/{elements.find('a').find('img')['src']}",
                'info': elements.find('p').text
            })
        return data

    @classmethod
    async def get_animate_video_json(cls, url: str) -> dict:
        """
        取得動漫影片資料。
        :param url: str -> 要爬的網址。
        :return: dict -> vpx 資料，如果官網 vpx 掛了就會回傳空字典。
        """
        return await cls.get_vpx_json(url=url, timeout=(60, 10))

    @classmethod
    async def download_ts_content(cls, ts_uri: str, host_list: list, video_720p: str):
        """
        下載 ts。
        :param ts_uri: str -> 要爬的網址。
        :param host_list: list -> 排序 weight 高到低陣列。
        :param video_720p: -> 720p 的資料字串。
        :return:
        """
        change = 0
        host_list_len = len(host_list)
        while True:
            ts_url = f"{host_list[0]['host']}{video_720p.replace('720p.m3u8', ts_uri)}"
            try:
                return await aiohttp_bytes(url=ts_url, timeout=(30, 10))
            except SERVER_AND_CLIENT_ERROR:
                if change > host_list_len - 1:
                    change = 0
                else:
                    change += 1
                print('ServerClientConnectionError')
            except Exception as error:
                print(error, 'download_ts_content')
                pass
            await asyncio.sleep(1)


if __name__ == '__main__':
    ...
