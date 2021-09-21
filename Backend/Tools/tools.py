from functools import reduce


def badname(name):
    """
    避免不正當名字出現導致資料夾或檔案無法創建。
    :param name: str -> 名字。
    :return: str -> 名字。
    """
    ban = r'\/:*?"<>|'
    return reduce(lambda x, y: x + y if y not in ban else x + ' ', name).strip()