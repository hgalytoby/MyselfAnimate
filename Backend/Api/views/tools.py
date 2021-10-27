from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'size'
    max_page_size = 50

    def next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def previous_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        return Response({
            'previous': self.previous_number(),
            'page': self.page.number,
            'next': self.next_number(),
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'data': data
        })
