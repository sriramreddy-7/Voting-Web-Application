"""VotingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from VotingProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('votinghome/', include('votinghome.urls')),
    path("",views.index,name="index"),
    path("register",views.register,name="register"),
    path("user_login",views.user_login,name="user_login"),
    path("user_dashboard",views.user_dashboard,name="user_dashboard"),
    path("user_logout",views.user_logout,name="user_logout"),
    path('success',views.success,name="success"),
    path('voter_register',views.voter_register,name="voter_register"),
    path("trail",views.trail,name="trail"),
    path('test2',views.test2,name='test2'),
    path('voter_login',views.voter_login,name="voter_login"),
    path('org_login',views.org_login,name="org_login"),
    path('admin_login',views.admin_login,name="admin_login"),
]
