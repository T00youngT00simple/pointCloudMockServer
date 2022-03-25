"""pointCloudMockServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from mock import views
from django.conf.urls import *



urlpatterns = [
    url(r'image/list/', views.getImageInfoList.as_view(), name="image-list"),
    url(r'image/(\w+)/details/', views.getImageInfoDetail.as_view(), name="image-detail"),

    url(r'image/(\w+)/cloud/data/', views.cloudData.as_view(), name="cloud-data"),

    url(r'image/(\w+)/sample/details/', views.samples.as_view(), name="sample"),

    url(r'image/tag/list/', views.tagList.as_view(), name="tagList"),

]


