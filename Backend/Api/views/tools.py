from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from Tools.tools import page_range


class MyPageNumberPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'size'
    max_page_size = 60

    def get_paginated_response(self, data):
        return Response(self.paginated(pag_obj=self.page, paginator=self.page.paginator, data=data))

    @staticmethod
    def paginated(pag_obj, paginator, data):
        return {
            'previous': pag_obj.previous_page_number() if pag_obj.has_previous() else None,
            'page': pag_obj.number,
            'next': pag_obj.next_page_number() if pag_obj.has_next() else None,
            'total_pages': paginator.num_pages,
            'count': paginator.count,
            'data': data,
            'range': page_range(page=pag_obj.number, total=paginator.num_pages)
        }