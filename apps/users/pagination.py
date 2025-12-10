from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'.lower()
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'status': True,
            'message': 'Data retrieved successfully',
            'status_code': 200,
            'page': self.page.number,
            'page_size': self.page.paginator.per_page,
            'total': self.page.paginator.count,
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages
            },
            'data': data
        })
