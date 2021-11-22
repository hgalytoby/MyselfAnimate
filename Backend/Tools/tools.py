import io
import asyncio
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

SERVER_AND_CLIENT_ERROR = (aiohttp.ClientConnectorCertificateError, aiohttp.ServerConnectionError,)


def badname(name: str) -> str:
    """
    避免不正當名字出現導致資料夾或檔案無法創建。
    :param name: str -> 名字。
    :return: str -> 名字。
    """
    ban = r'\/:*?"<>|'
    return reduce(lambda x, y: x + y if y not in ban else x + ' ', name).strip()


async def base_aiohttp_req(url: str, method: str, timeout: tuple, **kwargs):
    """
    異步請求的 base，依照 method 使用 .text or .json or .bytes。
    :param url: str -> 要爬的 url。
    :param method: str -> .text or .json or .bytes。
    :param timeout: tuple -> 設定請求與讀取時間。
    :param kwargs: .text or .json or .bytes 要用的參數。
    :return: str or dict or bytes -> .text or .json or .bytes。
    """
    _timeout = aiohttp.client.ClientTimeout(sock_connect=timeout[0], sock_read=timeout[1])
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url=url, headers=headers, timeout=_timeout) as res:
            return await getattr(res, method)(**kwargs)


async def aiohttp_text(url: str, timeout: tuple = (10, 10)) -> str:
    """
    用異步請求取得 text。
    :param url: str -> 要爬的 url。
    :param timeout: tuple -> 設定請求與讀取時間。
    :return:
    """
    return await base_aiohttp_req(url, method='text', timeout=timeout, encoding='utf-8', errors='ignore')


async def aiohttp_bytes(url: str, timeout=(10, 10)) -> bytes:
    """
    用異步請求取得 bytes。
    :param url: str -> 要爬的 url。
    :param timeout: tuple -> 設定請求與讀取時間。
    :return:
    """
    return await base_aiohttp_req(url, method='read', timeout=timeout)


async def aiohttp_json(url: str, timeout=(10, 10)) -> dict:
    """
    用異步請求取得 json。
    :param url: str -> 要爬的 url。
    :param timeout: tuple -> 設定請求與讀取時間。
    :return:
    """
    error_count = 0
    while True:
        try:
            return await base_aiohttp_req(url, method='json', timeout=timeout)
        except SERVER_AND_CLIENT_ERROR:
            if error_count == 20:
                return {}
            error_count += 1
            print('ServerClientConnectionError')
        await asyncio.sleep(3)


def req_bytes(url: str) -> bytes:
    """
    request 影像或圖片。
    :param url: str -> 要爬的 url。
    :return: bytes -> 影像或圖片
    """
    return requests.get(url=url, headers=headers).content


def use_io_get_image_format(image_bytes: bytes) -> str:
    """
    用 io 讀取 bytes(圖片)後，使用 Image 套件取得圖片的副檔名。
    :param image_bytes: bytes -> 讀取圖片後的 bytes。
    :return: str -> 圖片副檔名。
    """
    image_io = io.BytesIO(image_bytes)
    open_image = Image.open(image_io)
    image_type = open_image.format.lower()
    open_image.close()
    image_io.close()
    return image_type


@database_sync_to_async
def create_log(msg: str, action: str):
    LogModel.objects.create(msg=msg, action=action)


def page_range(page: int, total: int):
    x, y = divmod(page, 10)
    computed = (x + 1) * 10
    print('x', 'y', x, y, 'computed', computed)
    if total > computed:
        if y != 0:
            return list(range(x * 10 + 1, computed + 1))
        return list(range((x - 1) * 10 + 1, (x - 1) * 10 + 11))
    elif total == computed and 11 > page:
        return list(range(x + 1, total + 1))
    elif total == computed and y == 0 or computed > total:
        return list(range((x - 1) * 10 + 1, (x - 1) * 10 + 11))
    return list(range(x * 10 + 1, total + 1))
