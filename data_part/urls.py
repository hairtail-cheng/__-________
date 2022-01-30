"""bilibili_project URL Configuration

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
	path('up_update/', views.up_update, name='up_update'),
	path('up_detail/', views.up_detail, name='up_detail'),
	path('video/', views.videos, name='videos'),
	path('all_up/', views.all_up, name='all_up'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
