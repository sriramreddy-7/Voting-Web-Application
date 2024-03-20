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
    path('votingresult/', include('votingresult.urls')),
    path('votingcontact/', include('votingcontact.urls')),
    path('votingwebsite/', include('votingwebsite.urls')),
    path("",views.index,name="index"),
    path("register",views.register,name="register"),
    path("user_login",views.user_login,name="user_login"),
    path("user_dashboard",views.user_dashboard,name="user_dashboard"),
    path("user_logout",views.user_logout,name="user_logout"),
]
