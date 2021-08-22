from django.urls import path

from apps.system import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"user", views.UserModelView)
router.register(r"role", views.RoleModelView)
router.register(r"permission", views.PermissionModelView)


urlpatterns = [
    # jwt token 获取用户登录信息
    path("user/info", views.UserInfoView.as_view()),

    # vue生成用户对应菜单树
    path("menu_tree", views.MenuTreeView.as_view()),

    # 权限管理菜单树
    path("permission_tree", views.PermissionTreeView.as_view()),
]

urlpatterns = urlpatterns + router.urls