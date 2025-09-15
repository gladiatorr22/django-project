from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def add(request):
    n1=int(input("enter first number:"))
    n2=int(input("enter second number:"))
    res=n1+n2
    return HttpResponse(str(res))