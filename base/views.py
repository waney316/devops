# *-* coding: utf-8 *-*
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters


from base.pagination import PageNumberPagination


class BadeModelViewSet(ModelViewSet):
    """基类modelviewset"""
    pagination_class = PageNumberPagination  # 分页
    authentication_classes = [JSONWebTokenAuthentication]  # 认证
    permission_classes = [IsAuthenticated]  # 权限
    filter_backends = [OrderingFilter, SearchFilter, filters.DjangoFilterBackend]  # 查询排序过滤
