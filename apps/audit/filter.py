from django_filters import rest_framework as filters

from .models import AuditLogModel


class LoginLogFilter(filters.FilterSet):
    username = filters.CharFilter(method="custom_filter")

    def custom_filter(self, queryset, field_name, value):
        """通过前端请求body提取username过滤"""
        res = []
        for qs in queryset:
            if eval(qs.body).get(field_name) == value:
                res.append(qs)
        queryset = self.Meta.model.objects.filter(pk__in=[item.pk for item in res])
        return queryset

    class Meta:
        model = AuditLogModel
        fields = ["username", ]
