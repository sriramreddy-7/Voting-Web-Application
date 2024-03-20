from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def contact(request):
    return HttpResponse('<h1>This is Voting Website Contact Page.</h1>')