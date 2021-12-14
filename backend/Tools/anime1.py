from urllib.parse import unquote
import re
import requests
import asyncio
import aiohttp

from Tools.tools import aiohttp_text


def request_version():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }

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
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
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


if __name__ == '__main__':
    # asyncio.run(main())
    # request_version()
    pass