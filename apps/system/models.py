from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel

# 用户
class UserProfile(AbstractUser):
    """用户表扩展"""
    name = models.CharField(max_length=64, default="", verbose_name="中文姓名")
    phone = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=64, verbose_name="邮箱")
    avator = models.ImageField(upload_to="data/upload/%Y/%m", default="data/upload/default.jpeg", max_length=100,
                               null=True, blank=True)
    position = models.CharField(max_length=64, null=True, blank=True, verbose_name="职位")
    staff_id = models.IntegerField(null=True, blank=True, verbose_name="员工编号")
    job_status = models.BooleanField(default=True, verbose_name="员工在职状态")

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

    class Meta:
        db_table = "system_role"
        ordering = ["-id"]
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name


class UserRole(BaseModel):
    """用户和角色关联中间表"""
    user = models.IntegerField(verbose_name="用户ID")
    role = models.IntegerField(verbose_name="角色ID")

    class Meta:
        db_table = "system_user_role"


# 权限
class Permission(BaseModel):
    """映射vue路由菜单"""
    title = models.CharField(max_length=64, default="", verbose_name="标题")
    name = models.CharField(max_length=64, default="", verbose_name="名称")
    alias = models.CharField(max_length=64, default="", verbose_name="别名")
    icon = models.CharField(max_length=64, default="", verbose_name="图标")
    sort = models.IntegerField(default=0, verbose_name="展示顺序")
    parent = models.IntegerField(default=0, verbose_name="菜单层级")   # 0:顶级菜单 1:二级菜单  2:三级菜单
    type = models.IntegerField(default=0, verbose_name="权限类型")    # 1:菜单   2: 标签
    component = models.CharField(max_length=256, default="", verbose_name="组件类型")
    path = models.CharField(max_length=256, default="", verbose_name="路由路径")
    hidden = models.BooleanField(default=False, verbose_name="是否隐藏")
    external_link = models.BooleanField(default=False, verbose_name="是否外链")
    permission = models.CharField(max_length=128, default="", verbose_name="权限标识")
    cache = models.BooleanField(default=False, verbose_name="是否缓存")
    redirect = models.CharField(max_length=256, default="", verbose_name="跳转地址")

    class Meta:
        db_table = "system_permission"
        verbose_name = "权限信息"
        ordering = ["-id"]
        verbose_name_plural = verbose_name


class RolePermission(BaseModel):
    """角色权限关联中间表"""
    role = models.IntegerField(verbose_name="角色ID")
    permission = models.IntegerField(verbose_name="权限ID")

    class Meta:
        db_table = "system_role_permission"

