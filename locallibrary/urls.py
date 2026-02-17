"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.conf.urls.static import static    # 配置静态文件服务：如图片，CSS， js等静态文件
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),   # include("catalog.urls") 会导入 catalog 应用的 urls 进行进一步的路由
    path('', RedirectView.as_view(url='/catalog/')),    # 重定向如：输入：http://127.0.0.1:8000/，识别后重定向为 http://127.0.0.1:8000/catalog/ 然后又重定向为 catalog.urls继续后续域名匹配
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns  += [
    path('accounts/', include('django.contrib.auth.urls')),
]