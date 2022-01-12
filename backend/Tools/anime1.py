import time
import datetime
from urllib.parse import unquote
import re
import requests
import aiohttp
from bs4 import BeautifulSoup
from Tools.tools import aiohttp_text, badname, aiohttp_json, aiohttp_post_json
from Tools.urls import Anime1AnimateUrl, Anime1Api, NewAnime1AnimateUrl

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

animate_table = {
    '動畫名稱': 'name',
    '集數': 'episode',
    '年份': 'years',
    '季節': 'season',
    '字幕組': 'subtitle_group',
}


def request_version():
    r = requests.get(url='https://v.anime1.me/watch?v=MvAdi&autoplay=1', headers=headers)
    api_data = re.findall(r"send\S{2}(.*?)[']", r.text)[0]
    api_key, api_value = api_data.split('=')
    r = requests.post(url='https://v.anime1.me/api', headers=headers, data={api_key: unquote(api_value)})
    animate_url = f'https:{"".join(r.json().values())}'
    cookies = '; '.join(f'{_.name}={_.value}' for _ in r.cookies)
    headers.update({'cookie': cookies})
    with requests.get(url=animate_url, headers=headers, stream=True) as r:
        with open('test777.mp4', 'wb') as f:
            print(int(r.headers['Content-Length']) // (1024 * 10))
            for index, chunk in enumerate(r.iter_content(chunk_size=1024 * 10)):
                print(index)
                f.write(chunk)


async def main():
    _timeout = aiohttp.client.ClientTimeout(sock_connect=10, sock_read=10)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
        async with session.get(url='https://v.anime1.me/watch?v=MvAdi&autoplay=1', headers=headers,
                               timeout=_timeout) as res:
            r = await res.text(encoding='utf-8', errors='ignore')
            api_data = re.findall(r"send\S{2}(.*?)[']", r)[0]
            api_key, api_value = api_data.split('=')
    _timeout = aiohttp.client.ClientTimeout(sock_connect=10, sock_read=10)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
        async with session.post(url='https://v.anime1.me/api', headers=headers,
                                timeout=_timeout, data={api_key: unquote(api_value)}) as res:
            cookies = '; '.join(f'{v.key}={v.value}' for v in res.cookies.values())
            _ = await res.json()
            animate_url = f'https:{"".join(_.values())}'
    headers.update({'cookie': cookies})
    _timeout = aiohttp.client.ClientTimeout(sock_connect=10, sock_read=10)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
        async with session.get(url=animate_url, headers=headers, timeout=_timeout) as res:
            print(res.content_length)
            print(res.content_length // (1024 * 10))
            # print(len(await res.read()))
            with open('aiotest.mp4', 'wb') as fd:
                count = 0
                while True:
                    chunk = await res.content.read(1024 * 10)
                    print(count)
                    count += 1
                    if not chunk:
                        break
                    fd.write(chunk)


class Anime1:
    @staticmethod
    def old_get_home_animate_data() -> list:
        """
        本來官網是後端渲染
        2022/1/12
        改成用 Api 拿資料後渲染
        :return:
        """
        data = []
        res = requests.get(url=Anime1AnimateUrl, headers=headers)
        if res.ok:
            html = BeautifulSoup(res.text, 'lxml')
            title_array = []
            for title_element in html.find_all('tr', class_='row-1 odd'):
                for title in title_element.find_all('th'):
                    title_array.append(animate_table[title.text])
            title_array_len = len(title_array)
            for elements in html.find_all('tbody', class_='row-hover'):
                _ = {}
                for index, element in enumerate(elements.find_all('td')):
                    title_index = index % title_array_len
                    text = element.text
                    _.update({title_array[title_index]: text})
                    if title_index == 0:
                        _ = {
                            title_array[title_index]: badname(text),
                            'url': element.find("a")["href"]
                        }
                    if title_index == 4:
                        data.append(_)
                        _ = {}
        return data

    @staticmethod
    def get_home_animate_data() -> list:
        """
        取得 Anime1 首頁動漫資料。
        :return: dict -> {
            url: '?cat=數字'
            name: '動漫名字'
            episode: '集數'
            years: '年份'
            season: '季節'
            subtitle_group: '字幕組'
        }
        """
        data = []
        now = datetime.datetime.now()
        res = requests.get(
            url=NewAnime1AnimateUrl.format(f'{int(time.mktime(now.timetuple()) * 1e3 + now.microsecond / 1e3)}'),
            headers=headers)
        if res.ok:
            for item in res.json():
                data.append({
                    'url': f'?cat={item[0]}',
                    'name': badname(item[1]),
                    'episode': item[2],
                    'years': item[3],
                    'season': item[4],
                    'subtitle_group': item[5]
                })
        return data

    @classmethod
    def get_animate_info(cls, url: str, data: list) -> list:
        """
        取得動漫資料。
        ※ 如果有下一頁就會遞迴。
        :param url: str -> 網址。
        :param data: list ->
        :return: list -> [
            {
                published_updated_date: 發布日期 %Y-%m-%d,
                updated: 更新日其 %Y-%m-%d, ※ 最新的一集可能會沒有這個資料
                name: 集數名,
                url': 播放器 Url
            },
            {
                ...
            },
            ...
        ]
        """
        res = requests.get(url=url, headers=headers)
        if res.ok:
            html = BeautifulSoup(res.text, 'lxml')
            for elements in html.find_all('article'):
                _ = {}
                for index, element in enumerate(elements.find_all('time')):
                    if index == 0:
                        _.update({'published_updated_date': element.text})
                    else:
                        _.update({'updated': element.text})
                _.update({
                    'name': elements.find('h2', class_='entry-title').text.strip(),
                    'url': elements.find('button', class_='loadvideo')['data-src']
                })
                data.append(_)
            previous = html.find('div', class_='nav-previous')
            if previous:
                time.sleep(1)
                return cls.get_animate_info(url=previous.find('a')['href'], data=data)
        return data

    @staticmethod
    async def get_api_key_and_value(url: str) -> tuple:
        """
        取得拿影片 api 的 key 與 value。
        :param url: str -> 網址。
        :return: tuple -> (api_key, api_value)
        """
        res = await aiohttp_text(url=url)
        api_data = re.findall(r"send\S{2}(.*?)[']", res)[0]
        api_key, api_value = api_data.split('=')
        return api_key, api_value

    @staticmethod
    async def get_cookies_and_animate_url(api_key: str, api_value: str) -> tuple:
        """
        拿影片網址與需要的 Cookies
        :param api_key: str -> Api key。
        :param api_value: str -> Api value。
        :return: tuple -> (影片網址, 需要的 cookies)
        """
        data = {api_key: unquote(api_value)}
        res_json, cookies = await aiohttp_post_json(url=Anime1Api, data=data, cookie=True)
        animate_url = f'https:{"".join(res_json.values())}'
        return animate_url, cookies


if __name__ == '__main__':
    pass
