# *-* coding: utf-8 *-*

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """自定义分页形式"""
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100