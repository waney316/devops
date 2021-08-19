from rest_framework.views import APIView

from base.views import BadeModelViewSet
from base.response import json_api_response


class UserInfoView(APIView):
    """JWT token 获取用于信息"""
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        return json_api_response(code=0, message="success", data=None)
