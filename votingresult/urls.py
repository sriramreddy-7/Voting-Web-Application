from django.urls import include, path
from votingresult import views

urlpatterns = [

path('', views.result, name='result'),


]