
from django.urls import include, path
from votingwebsite import views


urlpatterns = [

path('', views.website, name='website'),


]