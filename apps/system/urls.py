from django.urls import path

from apps.system import views

urlpatterns = [
    path("user/info", views.UserInfoView.as_view()),

    # 用户
    path("user/", views.UserModelView.as_view({"get": "list", "post": "create"})),
    path("user/<int:pk>", views.UserModelView.as_view({"put": "update", "get": "retrieve", "delete": "destroy"})),

    # 角色
    path("role/", views.RoleModelView.as_view({"get": "list", "post": "create"})),
    path("role/<int:pk>", views.RoleModelView.as_view({"put": "update", "get": "retrieve", "delete": "destroy"})),

    # 权限
    path("permission/", views.PermissionModelView.as_view({"get": "list", "post": "create"})),
    path("permission/<int:pk>", views.PermissionModelView.as_view({"put": "update", "get": "retrieve", "delete": "destroy"})),
]