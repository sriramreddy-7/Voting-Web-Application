from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def result(request):
    return HttpResponse('<h1>This is Voting Website Result Page.</h1>')