from django.urls import path
from apps.audit import views

urlpatterns = [
    path("audit_log", views.AuditLogView.as_view({"get": "list"})),
    path("login_log", views.LoginLogView.as_view({"get": "list"})),
]
