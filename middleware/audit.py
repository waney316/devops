# *-* coding: utf-8 *-*
import json
from apps.audit.models import AuditLogModel

from django.utils.deprecation import MiddlewareMixin


class EventAuditMiddleware(MiddlewareMixin):
    """
    HTTP请求审计
    """

    RequestId = None

    def process_request(self, request):
        """接收请求"""
        # print(request.META)
        data = {
            "url": request.META["PATH_INFO"],
            "method": request.META["REQUEST_METHOD"],
            "query_string": request.META["QUERY_STRING"],
            "username": request.user.username,
        }

        # 如果存在代理
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # 如果有代理，获取真实IP
            data["remote_ip"] = x_forwarded_for.split(",")[0]
        else:
            data["remote_ip"] = request.META.get('REMOTE_ADDR')
        # request.environ["REMOTE_ADDR"]

        if request.META["REQUEST_METHOD"] in ["POST", "PUT"]:
            try:
                body = json.loads(request.body)
            except Exception as e:
                print("RequestEventAuditLog process_request", e.args)
                body = ""
        else:
            body = ""
        data["body"] = body
        request = AuditLogModel.objects.create(**data)
        self.RequestId = request.pk

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_template_response(self, request, response):
        request = AuditLogModel.objects.get(pk=self.RequestId)
        request.status_code = response.status_code
        request.save()
        return response

    def process_exception(self, request, exception):
        """异常"""
        request = AuditLogModel.objects.get(pk=self.RequestId)
        request.status_code = 500
        request.save()

    def process_response(self, request, response):
        """处理完成"""
        request = AuditLogModel.objects.get(pk=self.RequestId)
        request.status_code = response.status_code
        request.save()
        return response