import json
import time
import datetime
from urllib.parse import unquote
import re
import requests
import aiohttp
from bs4 import BeautifulSoup

# from Tools.db import DB
from Tools.tools import aiohttp_text, badname, aiohttp_post_json
from Tools.urls import Anime1AnimateUrl, Anime1Api, NewAnime1AnimateUrl, YoutubeUrl

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
                if '.pw/?cat=' not in item[1]:
                    _ = {
                        'url': item[0],
                        'name': badname(item[1]),
                    }
                else:
                    _ = {
                        'url': re.findall("cat=\d*", item[1])[0],
                        'name': badname(re.findall('>.*<', item[1])[0][1:-1]),
                    }
                data.append({
                    **_,
                    'episode': item[2],
                    'years': item[3],
                    'season': item[4],
                    'subtitle_group': item[5]
                })
        return data

    @classmethod
    def get_animate_info(cls, url: str, data: list) -> dict:
        """
        取得動漫資料。
        ※ 如果有下一頁就會遞迴。
        :param url: str -> 網址。
        :param data: list ->
        :return: dict ->
        {
        animate_name: str -> 動漫名字,
        episode_data: list -> 集數資料
        [{
                published_updated_date: 發布日期 %Y-%m-%d,
                updated: 更新日其 %Y-%m-%d, ※ 最新的一集可能會沒有這個資料
                name: 集數名,
                url': 播放器 Url
        },
        {
            ...
        },
        ...
        ]}
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
                })
                if elements.find('button', class_='loadvideo'):
                    _.update({'url': elements.find('button', class_='loadvideo')['data-src']})
                elif elements.find('div', {'class': 'youtubePlayer'}):
                    _.update({'url': f'{YoutubeUrl}{elements.find("div", {"class": "youtubePlayer"})["data-vid"]}'})
                elif elements.find('video').find('source'):
                    _.update({'url': elements.find('video').find('source')['src']})
                else:
                    _.update({'url': json.dumps({'url': url, 'data-vid': elements.find('video')['data-vid']})})
                data.append(_)
            previous = html.find('div', class_='nav-previous')
            if previous:
                return cls.get_animate_info(url=previous.find('a')['href'], data=data)
            return {'animate_name': html.find('h1', class_='page-title').text, 'episode_data': data}
        return {}

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

    @staticmethod
    async def get_cookies_and_animate_url_v2(api_key: str, api_value: str) -> tuple:
        """
        2022/1/23 發現官方改 Api 了。
        :param api_key: str -> Api key。
        :param api_value: str -> Api value。
        :return: tuple -> (影片網址, 需要的 cookies)
        """
        data = {api_key: unquote(api_value)}
        res_json, cookies = await aiohttp_post_json(url=Anime1Api, data=data, cookie=True)
        """
        {'l': '//korone.v.anime1.me/968/12b.mp4', 's': {'src': '//korone.v.anime1.me/968/12b.mp4', 'type': 'video/mp4'}}
        """
        return f'https:{res_json["l"]}', cookies

    @staticmethod
    async def get_api_key_and_value_v2(data):
        """
        2022/1/17 官方改 Api了。
        :param data:
        :return:
        """
        data = json.loads(data)
        res_html = DB.Cache.get_cache_data(f'api_key: {data["url"]}')
        if not res_html:
            res_html = await aiohttp_text(url=data['url'])
            DB.Cache.set_cache_data(key=f'api_key: {data["url"]}', data=res_html, timeout=600)
        html = BeautifulSoup(res_html, 'lxml')
        dom = html.find('video', {'data-vid': html.find('video')['data-vid']})
        return 'd', unquote(dom['data-apireq'])

    @staticmethod
    def get_season_list(season):
        res = requests.get(url=f'{Anime1AnimateUrl}/{season}', headers=headers)
        if res.ok:
            html = BeautifulSoup(res.text, 'lxml')
            entry_header = html.find('h2', class_='entry-title').text
            entry_title = html.find('th', colspan='7').text
            days = html.find('thead').find_all('tr')[1].text
            week_animate = html.find('tbody').find_all('tr')
            week_data = []
            for animates in week_animate:
                _ = []
                for animate in animates.find_all('td'):
                    if 'Anime1.me' not in animate.text:
                        if animate.find('a'):
                            _.append({'name': animate.text, 'url': animate.find('a')['href'].split('=')[1]})
                        else:
                            _.append({'name': animate.text, 'url': None})
                week_data.append(_)
            season_data = []
            for season_urls in html.find('div', class_='entry-content').find('p'):
                if '>> ' in season_urls.text:
                    if hasattr(season_urls, 'attrs'):
                        season_data.append({
                            'season': season_urls.text,
                            'url': True,
                        })
                    else:
                        season_data.append({
                            'season': season_urls.text,
                            'url': False,
                        })
            return {
                'header': entry_header,
                'title': entry_title,
                'days': days,
                'week_data': week_data[:-1],
                'season_data': season_data
            }
        return {}

    @staticmethod
    def get_home_season_url() -> dict:
        res = requests.get(url=Anime1AnimateUrl, headers=headers)
        if res:
            html = BeautifulSoup(res.text, 'lxml')
            menu_item = html.find_all('li', class_='menu-item-type-custom')[1]
            return {'url': menu_item.find('a')['href'], 'text': menu_item.text}
        return {}


if __name__ == '__main__':
    # season = Anime1.get_home_season_url()
    # print(Anime1.get_animate_info(url='https://anime1.me/?cat=823', data=[]))
    # print(Anime1.get_animate_info(url='https://anime1.pw/?cat=23', data=[]))
    # v = '%7B%22c%22%3A%221000%22%2C%22e%22%3A%222%22%2C%22t%22%3A1642680563%2C%22p%22%3A0%2C%22s%22%3A%22543c4500fb3f2006cde612ad5052024f%22%7D'
    print(unquote('https%3A//forum.gamer.com.tw/B.php%3Fbsn%3D60076'))
    print(unquote('https%3A%2F%2Fforum.gamer.com.tw%2FB.php%3Fbsn%3D60076'))
    # print(quote('https://forum.gamer.com.tw/B.php?bsn=60076'))
