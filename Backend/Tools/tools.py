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


async def base_aiohttp_req(url: str, method: str, timeout: tuple, **kwargs):
    _timeout = aiohttp.client.ClientTimeout(sock_connect=timeout[0], sock_read=timeout[1])
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url=url, headers=headers, timeout=_timeout) as res:
                return await getattr(res, method)(**kwargs)
    except aiohttp.ServerConnectionError as e:
        print('ServerConnectionError')
        return None
    except aiohttp.ClientConnectorCertificateError as e:
        print('ClientConnectorCertificateError')
        return None


async def aiohttp_text(url: str, timeout: tuple = (10, 10)) -> str:
    return await base_aiohttp_req(url, method='text', timeout=timeout, encoding='utf-8', errors='ignore')


async def aiohttp_bytes(url: str, timeout=(10, 10)) -> bytes:
    return await base_aiohttp_req(url, method='read', timeout=timeout)


async def aiohttp_json(url: str, timeout=(10, 10)) -> dict:
    return await base_aiohttp_req(url, method='json', timeout=timeout)


def req_bytes(url: str) -> bytes:
    return requests.get(url=url, headers=headers).content


def use_io_get_image_format(image_bytes: bytes) -> str:
    image_io = io.BytesIO(image_bytes)
    open_image = Image.open(image_io)
    image_type = open_image.format.lower()
    open_image.close()
    image_io.close()
    return image_type


@database_sync_to_async
def create_log(msg: str, action: str):
    LogModel.objects.create(msg=msg, action=action)
