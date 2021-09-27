import aiohttp
from channels.db import database_sync_to_async

from Tools.setup import *
from functools import reduce
from Database.models import LogModel

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52',
}


def badname(name):
    """
    避免不正當名字出現導致資料夾或檔案無法創建。
    :param name: str -> 名字。
    :return: str -> 名字。
    """
    ban = r'\/:*?"<>|'
    return reduce(lambda x, y: x + y if y not in ban else x + ' ', name).strip()


async def get_bytes(url):
    timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, timeout=timeout) as res:
            return await res.read()


async def get_text(url):
    timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, timeout=timeout) as res:
            return await res.text(encoding='utf-8', errors='ignore')


@database_sync_to_async
def create_log(msg, action):
    LogModel.objects.create(msg=msg, action=action)
