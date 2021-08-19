from django.db import transaction
from rest_framework.views import APIView

from base.views import BadeModelViewSet
from base.response import json_api_response

from apps.system.models import UserProfile, UserRole, RolePermission
from apps.system.seriazlizers import UserSerializer


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
                roles = request.data.get("roles", "")
                if roles:
                    request.data.pop("role")

                user = UserProfile.objects.create(**request.data)
                user_roles = []
                [ user_roles.append(UserRole(user=user, role=r)) for r in roles ]

                UserRole.objects.bulk_create(user_roles)
        except Exception as e:
            return json_api_response(code=-1, message=f"创建用户失败{e}")

        return json_api_response(code=0, message="success",)

