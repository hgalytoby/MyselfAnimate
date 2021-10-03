import io

import aiohttp
import requests
from PIL import Image
from channels.db import database_sync_to_async

from Tools.setup import *
from functools import reduce
from Database.models import LogModel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}


def badname(name: str) -> str:
    """
    避免不正當名字出現導致資料夾或檔案無法創建。
    :param name: str -> 名字。
    :return: str
    """
    ban = r'\/:*?"<>|'
    return reduce(lambda x, y: x + y if y not in ban else x + ' ', name).strip()


async def base_aiohttp_req(url, method, **kwargs):
    timeout = aiohttp.client.ClientTimeout(sock_read=10, sock_connect=10)
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url=url, headers=headers, timeout=timeout) as res:
                return await getattr(res, method)(**kwargs)
    except aiohttp.ServerConnectionError as e:
        print('ServerConnectionError')
        return None
    except aiohttp.ClientConnectorCertificateError as e:
        print('ClientConnectorCertificateError')
        return None


async def aiohttp_text(url):
    return await base_aiohttp_req(url, method='text', encoding='utf-8', errors='ignore')


async def aiohttp_bytes(url):
    return await base_aiohttp_req(url, method='read')


async def aiohttp_json(url):
    return await base_aiohttp_req(url, method='json')


def req_bytes(url):
    return requests.get(url=url, headers=headers).content


def use_io_get_image_format(image_bytes):
    image_io = io.BytesIO(image_bytes)
    open_image = Image.open(image_io)
    image_type = open_image.format.lower()
    open_image.close()
    image_io.close()
    return image_type


@database_sync_to_async
def create_log(msg: str, action: str):
    LogModel.objects.create(msg=msg, action=action)
