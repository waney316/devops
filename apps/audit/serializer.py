# *-* coding: utf-8 *-*
from apps.audit.models import AuditLogModel
from rest_framework.serializers import ModelSerializer


class AuditLogSerializer(ModelSerializer):
    """操作日志系列化"""
    class Meta:
        model = AuditLogModel
        fields = "__all__"


class LoginLogSerializer(ModelSerializer):
    """登录请求日志序列化"""
    class Meta:
        model = AuditLogModel
        fields = ['pk', 'remote_ip', 'username', 'status_code', 'create_time', "url", "body"]




