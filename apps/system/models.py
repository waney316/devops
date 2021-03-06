from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel


# 用户
class UserProfile(AbstractUser):
    """用户表扩展"""
    name = models.CharField(max_length=64, default="", verbose_name="中文姓名")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    email = models.EmailField(max_length=64, verbose_name="邮箱", null=True, blank=True)
    avator = models.ImageField(upload_to="data/upload/%Y/%m", default="data/upload/default.jpeg", max_length=100,
                               null=True, blank=True)
    position = models.CharField(max_length=64, null=True, blank=True, verbose_name="职位")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "system_user"
        ordering = ["-id"]
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


# 角色
class Role(BaseModel):
    name = models.CharField(max_length=64, verbose_name="角色")
    key = models.CharField(max_length=64, verbose_name="角色权限标识", default="")
    sort = models.PositiveSmallIntegerField(verbose_name="显示顺序", default=0)

    class Meta:
        db_table = "system_role"
        ordering = ["sort"]
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name


class UserRole(models.Model):
    """用户和角色关联中间表"""
    user = models.IntegerField(verbose_name="用户ID")
    role = models.IntegerField(verbose_name="角色ID")

    class Meta:
        db_table = "system_user_role"


# 权限
class Permission(models.Model):
    """映射vue路由菜单"""
    title = models.CharField(max_length=64, default="", blank=False, verbose_name="标题")
    name = models.CharField(max_length=64, default="", blank=True, verbose_name="名称")
    alias = models.CharField(max_length=64, default="", blank=True, verbose_name="别名")
    icon = models.CharField(max_length=64, default="", blank=True, verbose_name="图标")
    sort = models.IntegerField(default=0, verbose_name="展示顺序")  # 0->1->2
    parent = models.IntegerField(default=0, blank=True,verbose_name="菜单层级")  # 0:顶级菜单 1:二级菜单  2:三级菜单
    type = models.IntegerField(default=0, blank=True, verbose_name="权限类型")  # 1:菜单   2: 标签
    component = models.CharField(max_length=256, default="", blank=True, verbose_name="组件类型")
    path = models.CharField(max_length=256, default="", blank=True, verbose_name="路由路径")
    hidden = models.BooleanField(default=False, blank=True, verbose_name="是否隐藏")
    external_link = models.BooleanField(default=False, blank=True, verbose_name="是否外链")
    permission = models.CharField(max_length=128, default="", blank=True, verbose_name="权限标识")
    cache = models.BooleanField(default=False, blank=True, verbose_name="是否缓存")
    redirect = models.CharField(max_length=256, default="", blank=True, verbose_name="跳转地址")

    class Meta:
        db_table = "system_permission"
        verbose_name = "权限信息"
        ordering = ["-id"]
        verbose_name_plural = verbose_name


class RolePermission(models.Model):
    """角色权限关联中间表"""
    role = models.IntegerField(verbose_name="角色ID")
    permission = models.IntegerField(verbose_name="权限ID")

    class Meta:
        db_table = "system_role_permission"


class MailModel(models.Model):
    """邮件服务器相关配置"""
    smtp_host = models.CharField(max_length=128, verbose_name="smtp服务器")
    smtp_user = models.CharField(max_length=128, verbose_name="smtp用户")
    smtp_port = models.PositiveIntegerField(default=25, verbose_name="smtp端口")
    smtp_pass = models.CharField(max_length=512, verbose_name="smtp鉴权密码")

    class Meta:
        db_table = "system_mail"