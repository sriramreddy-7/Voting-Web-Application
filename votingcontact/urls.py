
from django.urls import include, path
from votingcontact import views
urlpatterns = [

path('', views.contact, name='contact'),


]