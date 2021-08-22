# *-* coding: utf-8 *-*
from apps.audit.models import AuditLogModel
from rest_framework.serializers import ModelSerializer

class AuditLogSerializer(ModelSerializer):

    class Meta:
        model = AuditLogModel
        fields = "__all__"
