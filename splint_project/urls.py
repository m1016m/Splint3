"""
URL configuration for splint_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from splint_app import views as splint_views # 導入 app 的 views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splint_views.home_view, name='home'), # 首頁
    path('accounts/signup/', splint_views.signup_view, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), # 使用 next_page 在 settings.py LOGOUT_REDIRECT_URL 指定
    path('course/', include('splint_app.urls')), # 將 course 相關的 URL 包含進來
    path('ckeditor/', include('ckeditor_uploader.urls')), # 加入 ckeditor 上傳的 URL
]
from django.conf import settings # 新增
from django.conf.urls.static import static # 新增
# 在開發模式下，讓 Django 處理 MEDIA 文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)