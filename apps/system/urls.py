from django.urls import path

from apps.system import views

urlpatterns = [
    path("user/info", views.UserInfoView.as_view()),

    # 用户url
    path("user/", views.UserModelView.as_view({"get": "list", "post": "create"})),
    path("user/<int:pk>", views.UserModelView.as_view({"put": "update", "get": "retrive", "delete": "destroy"})),
]