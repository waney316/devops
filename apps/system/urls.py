from django.urls import path

from apps.system import views

urlpatterns = [
    path("user/info", views.UserInfoView.as_view(),)
]