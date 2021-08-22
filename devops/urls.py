"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated

from apps.system import urls as system_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    # jwt token
    path(f"{settings.API_VERSION}/jwt-token", obtain_jwt_token),

    # api docs
    path(f"{settings.API_VERSION}/docs", include_docs_urls(title="devops api", permission_classes=[IsAuthenticated])),

    # system
    path(f'{settings.API_VERSION}/system/', include(system_urls))
]
