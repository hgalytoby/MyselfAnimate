import asyncio

import requests
import aiohttp
from bs4 import BeautifulSoup

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
                result = {}
                elements = html.find('div', id='tabSuCvYn')
                for index, element in enumerate(elements.find_all('div', class_='module cl xl xl1')):
                    animate_data = []
                    for animate in element:
                        animate_data.append({
                            'name': animate.find('a')['title'],
                            'url': animate.find('a')['href'],
                            'update_color': animate.find('span').find('font').find('font')['style'],
                            'update': animate.find('span').find('font').text,
                        })
                    result.update({week[index]: animate_data})
                # res.close()
                return result
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
            data = {'url': url}
            data.update({'name': badname(html.find('title').text.split('【')[0])})
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
        for index, elements in enumerate(html.find_all('div', {'class': 'tab-title title column cl'})):
            year_list = []
            for i, element in enumerate(elements.find_all('div', {'class': 'block move-span'})):
                year_month_title = element.find('span', {'class': 'titletext'}).text
                season_list = []
                for k in element.find_all('a'):
                    season_list.append({'name': k['title'], 'url': f"https://myself-bbs.com/{k['href']}"})
                year_list.append({'title': year_month_title, 'data': season_list})
            data.append({'data': year_list})
        # res.close()
        # for i in data:
        #     for k, v in i.items():
        #         for j in v:
        #             for k1, v1 in j.items():
        #                 print(k1, v1)
        return {'data': data}


async def main():
    tasks = [asyncio.create_task(Myself.week_animate())]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    # asyncio.run(main())
    # print(badname(r'\12/47:*8?9"<4>5|1'))
    Myself.finish_list()

    pass
