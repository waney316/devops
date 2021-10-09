from base.views import BadeModelViewSet
from base.response import json_api_response

from apps.audit.models import AuditLogModel
from apps.audit.serializer import AuditLogSerializer, LoginLogSerializer
from apps.audit.filter import LoginLogFilter

from django.conf import settings

# 区分登录请求
REQUEST_TAGS = [f"/{settings.API_VERSION}/jwt-token"]


class AuditLogView(BadeModelViewSet):
    """操作日志"""
    queryset = AuditLogModel.objects.exclude(url__in=REQUEST_TAGS)
    serializer_class = AuditLogSerializer
    search_fields = ("url",)  # url模糊搜索
    filterset_fields = ("method", "username",)  # method, username精确搜索


class LoginLogView(BadeModelViewSet):
    queryset = AuditLogModel.objects.filter(url__in=REQUEST_TAGS)
    serializer_class = LoginLogSerializer
    filterset_class = LoginLogFilter

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                for qs in serializer.data:
                    body = eval(qs.pop("body"))
                    # replace login usename to request body username
                    qs["username"] = body.get("username")
                    # add login status
                    qs["status"] = "success" if qs.get("status_code") == 200 else "failed"
                    qs["body"] = {"username": body.get("username"), "password": "*"} if qs.get(
                        "status_code") == 200 else body
                response_data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                response_data = serializer.data
        except Exception as e:
            return json_api_response(code=-1, message=f"获取登录日志错误{e}")

        return json_api_response(code=0, message="获取登录日志成功", data=response_data)
