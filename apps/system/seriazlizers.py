from rest_framework.serializers import ModelSerializer

from apps.system import models


class UserSerializer(ModelSerializer):
    """用户信息序列化"""

    class Meta:
        model = models.UserProfile
        exclude  = ("password",)


class RoleSerializer(ModelSerializer):
    """角色信息序列化"""

    class Meta:
        model = models.Role
        fields = "__all__"


class PermissionSerializer(ModelSerializer):
    """权限信息序列化"""

    class Meta:
        model = models.Permission
        fields = "__all__"