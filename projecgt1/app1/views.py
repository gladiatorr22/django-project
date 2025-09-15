from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def view1(request):
    s="welcome to django"
    return HttpResponse(s)

def myname(request):
    name="my name is django"
    return HttpResponse(name)