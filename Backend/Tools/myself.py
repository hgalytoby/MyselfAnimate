import asyncio
import io
from PIL import Image
import m3u8
import requests
import aiohttp
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
import django
import os

from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from Database.models import FinishAnimateModel
from Tools.tools import badname

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
    '播出集數': 'episodes',
    '原著作者': 'author',
    '官方網站': 'official_website',
    '備注': 'remarks',
}


class Myself:
    @staticmethod
    def week_animate() -> dict:
        """
        爬首頁的每周更新表。
        :return: Dict。
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
        :return: dict -> 所有需要的資料。
        {
            url: 網址,
            video: [{name: 第幾集, url: 網址}]
            name: 名字,
            anime_type: 作品類型,
            premiere_date: 首播日期,
            number_of_episodes_broadcast: 播出集數,
            author: 原著作者,
            official_website: 官方網站,
            remarks: 備注,
        }
        """
        try:
            res = requests.get(url=url, headers=headers, timeout=(5, 5))
            html = BeautifulSoup(res.text, features='lxml')
            data = {'url': url, 'name': badname(html.find('title').text.split('【')[0])}
            permission = html.find('div', id='messagetext')
            if permission:
                data.update({'permission': permission.text.strip()})
            total = list()
            for i in html.select('ul.main_list'):
                for j in i.find_all('a', href='javascript:;'):
                    title = j.text
                    for k in j.parent.select("ul.display_none li"):
                        a = k.select_one("a[data-href*='v.myself-bbs.com']")
                        if k.select_one("a").text == '站內':
                            url = a["data-href"].replace('player/play', 'vpx').replace("\r", "").replace("\n", "")
                            total.append({'name': badname(name=title), 'url': url})
            data.update({'video': total})
            for i in html.find_all('div', class_='info_info'):
                for j, m in enumerate(i.find_all('li')):
                    text = m.text
                    key, value = text.split(': ')[0], text.split(': ')[1]
                    data.update({animate_table[key]: value})
            for i in html.find_all('div', class_='info_introduction'):
                for j in i.find_all('p'):
                    data.update({'synopsis': j.text})
            for i in html.find_all('div', class_='info_img_box fl'):
                for j in i.find_all('img'):
                    data.update({'image': j['src']})
            res.close()
            return data
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    def finish_list():
        """
        爬完結列表頁面的動漫資訊
        :return: Dict。
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
    def get_request_json(url):
        res = requests.get(url=url, headers=headers)
        try:
            if res.ok:
                return res.json()
            return {}
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    def get_vpx_json(url):
        res = requests.get(url=url, headers=headers)
        try:
            if res.ok:
                return res.json()
            return {}
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    def get_m3u8_data(url):
        try:
            res = requests.get(url=url, headers=headers)
            if res.ok:
                try:
                    return m3u8.loads(res.text)
                except BaseException as error:
                    print(f'get_m3u8 error: {error}')
                    return {}
            return {}
        except requests.exceptions.RequestException as error:
            return {}

    @staticmethod
    async def finish_animate_total_page(url, get_res_text=False):
        """
        爬完結動漫總頁數多少。
        :param url: str -> 要爬的網址。
        :param get_html: boor -> True = 將 requests.text 返回。
        :return: dict -> 該頁的資料。
        {
            total_page: 總頁數,
            html: 該頁面的資料。
        }
        """
        timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, timeout=timeout) as res:
                res_text = await res.text(encoding='utf-8', errors='ignore')
                html = BeautifulSoup(res_text, 'lxml')
                page_data = html.find('div', class_='pg').find('a', class_='last').text
                if page_data and get_res_text:
                    return {'total_page': int(page_data.replace('... ', '')), 'res_text': res_text}
                else:
                    return {'total_page': int(page_data.replace('... ', ''))}

    @staticmethod
    async def finish_animate_page_data(url, res_text=None):
        """
        完結動漫頁面的動漫資料。
        :param url: str -> 要爬的網址。
        :param res_text: str -> 給完結動漫某頁的HTML，就不用在 requests 了。
        :return: dict -> 該頁的資料。
        {
            動漫名字:{
                url: 動漫網址,
                img: 圖片網址,
            }
        }
        """
        if not res_text:
            timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers, timeout=timeout) as res:
                    res_text = await res.text(encoding='utf-8', errors='ignore')
        html = BeautifulSoup(res_text, 'lxml')
        data = []
        for elements in html.find_all('div', class_='c cl'):
            data.append({
                'url': f"https://myself-bbs.com/{elements.find('a')['href']}",
                'name': badname(elements.find('a')['title']),
                'image': f"https://myself-bbs.com/{elements.find('a').find('img')['src']}"
            })
        return data

    @staticmethod
    @database_sync_to_async
    def save_finish_animate_data(animate):
        image_io = io.BytesIO(animate['image'])
        open_image = Image.open(image_io)
        image_type = open_image.format.lower()
        open_image.close()
        image_io.close()
        model = FinishAnimateModel()
        model.name = animate['name']
        model.url = animate['url']
        model.image.save(f'{animate["name"]}.{image_type}', ContentFile(animate['image']))

    @staticmethod
    async def get_image(img_url):
        timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=img_url, headers=headers, timeout=timeout) as res:
                return await res.read()

    @staticmethod
    async def create_finish_animate_data_task(animate):
        animate['image'] = await Myself.get_image(img_url=animate['image'])
        await Myself.save_finish_animate_data(animate)

    @staticmethod
    async def create_finish_animate_data(data):
        tasks = []
        for animate in data:
            if not await database_sync_to_async(list)(FinishAnimateModel.objects.filter(url=animate['url'])):
                tasks.append(asyncio.create_task(Myself.create_finish_animate_data_task(animate)))
        if tasks:
            await asyncio.wait(tasks)


async def main(_):
    await Myself.create_finish_animate_data(_)


if __name__ == '__main__':
    # asyncio.run(main(Myself.finish_animate_page_data(url='https://myself-bbs.com/forum-113-1.html')))
    pass
