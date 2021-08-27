from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
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
                roles = request.data.pop("roles", None)

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                # 如果存在角色关联：
                if roles:
                    user_roles = [UserRole(user=serializer.data["id"], role=r) for r in roles]
                    UserRole.objects.bulk_create(user_roles)

        except Exception as e:
            return json_api_response(code=-1, message=f"创建用户失败{e}")

        return json_api_response(code=0, message=f"创建用户成功", data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新用户信息"""
        try:
            with transaction.atomic():
                roles = request.data.pop("roles", None)

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
                    user_roles = [UserRole(user=serializer.data["id"], role=r_id) for r_id in roles]
                    # 更新用户权限
                    UserRole.objects.bulk_create(user_roles)
        except Exception as e:
            return json_api_response(code=-1, message=f"更新用户失败{e}", data=None)

        return json_api_response(code=0, message="更新用户成功", data=serializer.data)

    def list(self, request, *args, **kwargs):
        """获取用户信息列表"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                for user in serializer.data:
                    user_roles = list(UserRole.objects.filter(user=user.get("id")).values_list("role"))
                    user["roles"] = [r[0] for r in user_roles]
                user_data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                user_data = serializer.data

        except Exception as e:
            return json_api_response(code=-1, message=f"获取用户信息列表失败{e}")

        return json_api_response(code=0, message="获取用户信息列表成功", data=user_data)

    def retrieve(self, request, *args, **kwargs):
        """获取单个用户信息"""
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

    def destroy(self, request, *args, **kwargs):
        """删除单个用户信息"""
        try:
            with transaction.atomic():
                instance = self.get_object()
                # 删除用户时删除角色表中数据
                UserRole.objects.filter(user=instance.id).delete()
                self.perform_destroy(instance)
        except Exception as e:
            return json_api_response(code=-1, message=f"删除用户失败{e}")

        return json_api_response(code=0, message="删除用户信息成功")


class RoleModelView(BadeModelViewSet):
    """
    角色管理
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ("name", "key")

    def list(self, request, *args, **kwargs):
        """查询角色时获取角色关联权限"""
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                for role in serializer.data:
                    role["permissions"] = [p[0] for p in
                                           RolePermission.objects.filter(role=role["id"]).values_list("permission")]
                role_data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                role_data = serializer.data
        except Exception as e:
            return json_api_response(code=-1, message=f"获取角色列表信息失败{e}")
        return json_api_response(code=0, message="获取角色列表信息成功", data=role_data)

    @action(methods=["put"], detail=True, url_path="role_permission", url_name="role_permission")
    def role_permission(self, request, *args, **kwargs):
        """更新角色权限"""
        try:
            with transaction.atomic():
                print(request.data)
                permissions = request.data.pop("permission", None)
                instance = self.get_object()

                if permissions:
                    RolePermission.objects.filter(permission__in=permissions, role=instance.id).delete()
                    role_permissions = [RolePermission(role=instance.id, permission=p) for p in permissions]
                    RolePermission.objects.bulk_create(role_permissions)

        except Exception as e:
            return json_api_response(code=-1, message=f"更新角色权限失败{e}")
        return json_api_response(code=0, message="更新角色权限成功")


class PermissionModelView(BadeModelViewSet):
    """
    权限管理
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ("title",)


class MenuTreeView(APIView):
    """
    获取当前用户角色对应菜单树
    """

    def format_menu(self, menu):
        """
        格式化菜单树
        :param menu: 每个递归遍历的菜单
        :return:
        """
        return {
            "path": menu["path"],
            "component": menu["component"],
            "title": menu["title"],
            "icon": menu["icon"]
        }

    def recursion_menu(self, childs, parent_id, role_permissions):
        """
        生成菜单树
        :param id: 父级菜单id
        :param menu: 父级菜单
        :return:
        """
        childMenus = []  # 返回的菜单数据

        for child in childs:
            # 如果当前节点id不在权限菜单里
            if child["id"] not in role_permissions:
                continue

            child_data = self.format_menu(child)
            _childs = Permission.objects.filter(parent=child["id"], type=1).values() #当前节点是否存在下一集菜单
            if _childs:
                _childs_data = []
                _childs_data.append(self.recursion_menu(_childs, child["id"], role_permissions))
                child_data["children"] = _childs_data
            childMenus.append(child_data)
        return childMenus


    def get(self, request, *args, **kwargs):
        user = UserProfile.objects.get(id=request.user.id)
        try:
            role_permissions = []
            # 如果用户为管理员,返回全部菜单
            if user.is_superuser:
                user_permission = list(Permission.objects.filter(type=1, parent=0).order_by("sort").values())
            else:
                user_roles = [role[0] for role in UserRole.objects.filter(user=user.id).values_list("role")]
                role_permissions = list(set(
                    [perm[0] for perm in RolePermission.objects.filter(role__in=user_roles).values_list("permission")]))
                user_permission = list(
                    Permission.objects.filter(type=1, parent=0, id__in=role_permissions ).order_by("sort").values())

            tree_data = []
            for menu in user_permission:
                menu_data = self.format_menu(menu)
                child_menus = Permission.objects.filter(parent=menu["id"]).values()
                if child_menus:
                # 根据权限数据生成vue可识别的格式
                    menu_data["children"] = self.recursion_menu(child_menus, menu["id"], role_permissions)

                tree_data.append(menu_data)
        except Exception as e:
            return json_api_response(code=-1, message=f"生成菜单树失败{e}")

        return json_api_response(code=0, message="生成菜单树成功", data=tree_data)


class UserPermission(APIView):
    """获取当前请求用户的标签权限"""
    def get(self, request):
        """获取当前用户页面标签权限"""
        try:
            user = UserProfile.objects.get(pk=request.user.id)
            if user.is_superuser:
                user_permission = ["*:*:*"]
            else:
                # 查询用户关联角色
                user_roles = [role[0] for role in UserRole.objects.filter(user=user.id).values_list("role")]
                # 查询角色关联权限
                permissions = [p[0] for p in
                               RolePermission.objects.filter(role__in=user_roles).values_list("permission")]
                # 根据权限id返回菜单数据
                user_permission = [p[0] for p in list(
                    Permission.objects.filter(id__in=permissions, type=2).exclude(permission="").values_list(
                        "permission"))]

        except Exception as e:
            return json_api_response(code=-1, message=f"查询用户权限失败{e}")

        return json_api_response(code=0, message="查询用户权限成功", data=user_permission)



class PermissionTreeView(APIView):
    """权限管理权限树"""

    def recursion_menu(self, menu):
        if menu:
            children_list = Permission.objects.filter(parent=menu["id"]).order_by("sort").values()
            if children_list:
                menu["children"] = children_list
                for m in children_list:
                    self.recursion_menu(m)
        return menu

    def get(self, request, *args, **kwargs):
        try:
            title = request.GET.get("title", None)
            permission_data = []
            if not title:
                menus_list = Permission.objects.filter(parent=0).order_by("sort").values()
                for menu in menus_list:
                    permission_data.append(self.recursion_menu(menu))
            else:
                permission_data = list(Permission.objects.filter(title__icontains=title).values())
        except Exception as e:
            return json_api_response(code=-1, message=f"获取权限列表失败{e}")

        return json_api_response(code=0, message="获取权限列表成功", data=permission_data)
