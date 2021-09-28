import aiohttp
from channels.db import database_sync_to_async

from Tools.setup import *
from functools import reduce
from Database.models import LogModel

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52',
}


def badname(name: str) -> str:
    """
    避免不正當名字出現導致資料夾或檔案無法創建。
    :param name: str -> 名字。
    :return: str
    """
    ban = r'\/:*?"<>|'
    return reduce(lambda x, y: x + y if y not in ban else x + ' ', name).strip()


async def base_req_res(url, method, **kwargs):
    timeout = aiohttp.client.ClientTimeout(sock_read=5, sock_connect=5)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, timeout=timeout) as res:
            return await getattr(res, method)(**kwargs)


async def req_res_text(url):
    return await base_req_res(url, method='text', encoding='utf-8', errors='ignore')


async def req_res_bytes(url):
    return await base_req_res(url, method='read')


async def req_res_json(url):
    return await base_req_res(url, method='json')


@database_sync_to_async
def create_log(msg: str, action: str):
    LogModel.objects.create(msg=msg, action=action)
