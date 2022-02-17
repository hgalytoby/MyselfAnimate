from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]
        return tags


class BaseSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='所有',
                                                           operation_description='''
                                                           ''')}
    c = {'name': 'create', 'decorator': swagger_auto_schema(operation_summary='新增',
                                                            operation_description='')}
    r = {'name': 'retrieve', 'decorator': swagger_auto_schema(operation_summary='單個',
                                                              operation_description='- url id: ')}
    u = {'name': 'update', 'decorator': swagger_auto_schema(operation_summary='更新',
                                                            operation_description='- url id: ')}
    d = {'name': 'destroy', 'decorator': swagger_auto_schema(operation_summary='刪除',
                                                             operation_description='- url id: ')}


class MyselfWeekAnimateSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 首頁每週動漫資料',
                                                           operation_description='''
                                                            ''')}


class MyselfAnimateInfoSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 動漫資料',
                                                           operation_description='''
                                                            ''')}


class MyselfUrlAnimateSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 搜尋動漫',
                                                           operation_description='''
                                                            ''')}


class MyselfFinishListSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 完結列表',
                                                           operation_description='''
                                                            ''')}


class MyselfFinishAnimateSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 已下載的完結動漫資料',
                                                           operation_description='''
                                                            ''')}


class MyselfAnimateEpisodeInfoEpisodeSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Myself 動漫集數資料',
                                                           operation_description='''
                                                            ''')}

class MyselfAnimateEpisodeDoneSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='所有 Myself 動漫下載完畢資料',
                                                           operation_description='''
                                                            ''')}

class MyselfDestroyManyAnimateSwagger:
    d = {'name': 'destroy', 'decorator': swagger_auto_schema(operation_summary='刪除多筆已下載動漫資料',
                                                             operation_description='')}


class Anime1AnimateSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='所有 Anime1 首頁動漫資料',
                                                           operation_description='''
                                                            ''')}


class Anime1AnimateInfoSwagger:
    c = {'name': 'create', 'decorator': swagger_auto_schema(operation_summary='新增 Anime1 動漫資料',
                                                            operation_description='''
                                                            ''')}


class Anime1AnimateInfoEpisodeSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='所有 Anime1 首頁動漫集數資料',
                                                           operation_description='''
                                                            ''')}


class Anime1AnimateEpisodeDoneSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='所有 Anime1 動漫下載完畢資料',
                                                           operation_description='''
                                                            ''')}


class Anime1MenuSeasonSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Anime1 首頁季番名稱與網址',
                                                           operation_description='''
                                                            ''')}


class Anime1SeasonSwagger:
    rs = {'name': 'list', 'decorator': swagger_auto_schema(operation_summary='Anime1 所有季番資料',
                                                           operation_description='''
                                                            ''')}


class Anime1DestroyManyAnimateSwagger:
    d = {'name': 'destroy', 'decorator': swagger_auto_schema(operation_summary='刪除多筆已下載動漫資料',
                                                             operation_description='')}
