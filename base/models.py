# -*- coding: utf-8 -*-

from django.db import models


class BaseModel(models.Model):
    """基础model表"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    remarks = models.CharField(max_length=1024, null=True, blank=True, verbose_name="备注信息")

    class Meta:
        abstract = True
