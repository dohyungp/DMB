"""untitled8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import (
    profile_update,
    profile_create,
    profile_detail,
    profile_list,
)
urlpatterns = [
    url(r'^$', profile_list, name='list'),
    url(r'^create/$', profile_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', profile_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', profile_update, name='update'),
]