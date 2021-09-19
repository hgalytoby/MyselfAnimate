import asyncio
import requests
import aiohttp
from bs4 import BeautifulSoup

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
                return result
        except requests.exceptions.RequestException as error:
            return {}



async def main():
    tasks = [asyncio.create_task(Myself.week_animate())]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
