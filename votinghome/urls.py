from django.contrib import admin
from django.urls import include, path
from votinghome import views
urlpatterns = [

path('', views.home, name='home'),



]