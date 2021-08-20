from rest_framework.serializers import ModelSerializer

from apps.system import models


class UserSerializer(ModelSerializer):
    """用户信息序列化"""

    class Meta:
        model = models.UserProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


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