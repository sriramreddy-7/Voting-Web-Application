from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def website(request):
    return HttpResponse('<h1>This is Voting Website Home Page.</h1>')