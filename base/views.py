# *-* coding: utf-8 *-*
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters

from base.pagination import CustomPagination
from base.response import json_api_response


class BadeModelViewSet(ModelViewSet):
    """基类modelviewset"""
    pagination_class = CustomPagination  # 分页
    authentication_classes = [JSONWebTokenAuthentication]  # 认证
    permission_classes = [IsAuthenticated]  # 权限
    filter_backends = [OrderingFilter, SearchFilter, filters.DjangoFilterBackend]  # 查询排序过滤
    search_fields = []
    filterset_fields = []


    def create(self, request, *args, **kwargs):
        """创建"""
        response = super().create(request, *args, **kwargs)
        return json_api_response(code=0, message="success", data=response.data)


    def list(self, request, *args, **kwargs):
        """获取全部数据"""
        response = super().list(request, *args, **kwargs)
        return json_api_response(code=0, message="success", data=response.data)


    def retrieve(self, request, *args, **kwargs):
        """获取单个数据"""
        response = super().retrieve(request, *args, **kwargs)
        return json_api_response(code=0, message="success", data=response.data)


    def update(self, request, *args, **kwargs):
        """更新"""
        response = super().update(request, *args, **kwargs)
        return json_api_response(code=0, message="success", data=response.data)


    def destroy(self, request, *args, **kwargs):
        """删除"""
        response = super().destroy(request, *args, **kwargs)
        return json_api_response(code=0, message="success", data=response.data)
