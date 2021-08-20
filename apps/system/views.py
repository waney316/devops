from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from base.views import BadeModelViewSet
from base.response import json_api_response

from apps.system.models import UserProfile, UserRole, RolePermission, Role, Permission
from apps.system.seriazlizers import UserSerializer, RoleSerializer, PermissionSerializer


class UserInfoView(APIView):
    """JWT token 获取用于信息"""
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            u = UserProfile.objects.get(pk=user.id)
        except UserProfile.DoesNotExist:
            return json_api_response(code=-1, message=f"{user} not exist")

        user_info = UserSerializer(u)
        return json_api_response(code=0, message="success", data=user_info.data)


class UserModelView(BadeModelViewSet):
    """
    用户信息
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    search_fields = ("name", "username", "phone")

    def create(self, request, *args, **kwargs):
        """创建用户的时候关联角色"""
        try:
            with transaction.atomic():
                roles = request.data.pop("roles", "")
                password = request.data.get("password")
                if password:
                    request.data.update({"password": make_password(password)})
                user = UserProfile.objects.create(**request.data)
                user_roles = []
                # 如果存在角色关联：
                if roles:
                    [ user_roles.append(UserRole(user=user.id, role=r)) for r in roles ]
                    UserRole.objects.bulk_create(user_roles)

        except Exception as e:
            return json_api_response(code=-1, message=f"创建用户失败{e}")

        return json_api_response(code=0, message=f"创建用户成功",data=user.id)

    def update(self, request, *args, **kwargs):
        """更新用户信息"""
        try:
            with transaction.atomic():
                roles = request.data.pop("roles")

                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                if roles:
                    UserRole.objects.filter(user=serializer.data["id"]).delete()
                    user_roles = []
                    for r_id in roles:
                        user_roles.append(UserRole(user=serializer.data["id"], role=r_id))
                    # 更新用户权限
                    UserRole.objects.bulk_create(user_roles)
        except Exception as e:
            return json_api_response(code=-1, message=f"更新用户失败{e}", data=None)
        return json_api_response(code=0, message="更新用户成功", data=serializer.data)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            user_roles = []
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                for user in serializer.data:
                    user_roles =  list(UserRole.objects.filter(user=user.get("id")).values_list("role"))
                    user["roles"] = [r[0] for r in user_roles]
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

        except Exception as e:
            return json_api_response(code=-1, message=f"获取用户信息列表失败{e}")
        return json_api_response(code=0, message="获取用户信息列表成功", data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            # 获取用户关联的权限
            user_roles = [role[0] for role in UserRole.objects.filter(user=instance.id).values_list("role")]
            serializer.data.update({"roles": user_roles})
            user_data = serializer.data
            user_data["roles"] = user_roles
        except Exception as e:
            return json_api_response(code=-1, message=f"获取用户信息失败{e}")
        return json_api_response(code=0, message=f"获取用户信息成功", data=user_data)



class RoleModelView(BadeModelViewSet):
    """
    角色管理
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ("name", )




class PermissionModelView(BadeModelViewSet):
    """
    权限管理
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ("title",)