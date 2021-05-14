from rest_framework import pagination, response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 9

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count, # すべてのデータ数
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size, # 1ページ内の件数
        })

