# *-* coding: utf-8 *-*

from rest_framework.response import Response

"""
code: 0 正常
code: -1 异常
"""

def json_api_response(code, message, data=None):
    """自定义请求返回格式"""
    return Response({
        "code": code,
        "message": message,
        "data": data
    })



def jwt_response_payload(token, user=None, request=None):
    """自定义jwt token返回"""
    return {
        "code": 0,
        "message":"success",
        "data": token
    }
