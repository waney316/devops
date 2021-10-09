from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from apps.system import models


class UserSerializer(ModelSerializer):
    """用户信息序列化"""

    class Meta:
        model = models.UserProfile
        # fields = "__all__"
        exclude = ("groups", "user_permissions",)
        extra_kwargs = {
            'password': {'required': False}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            validated_data["password"] = make_password(password)

        return self.Meta.model.objects.create(**validated_data)


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
        ordering = ["id"]
        extra_kwargs = {
            'title': {'required': True}
        }


class MailSerializer(ModelSerializer):
    """邮件服务器序列化"""
    class Meta:
        model = models.MailModel
        fields = "__all__"
        ordering = ["i"]

