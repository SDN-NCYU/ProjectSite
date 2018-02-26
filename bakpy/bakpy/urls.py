"""bakpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from excuse import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^Protect.html/', views.Protect),
    url(r'^mymodel.html/', views.mymodel),
    url(r'^NewProject.html/', views.NewProject),
    url(r'^WhiteList.html/', views.WhiteList),
    url(r'^BlackList.html/', views.BlackList),
    url(r'^AttackList.html/', views.AttackList),
    url(r'^login.html/', views.login),
    url(r'^logintest.html/', views.logintest),
    url(r'^logout.html/', views.logout), 

    ]
