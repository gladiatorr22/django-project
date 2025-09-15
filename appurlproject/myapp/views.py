from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view1(request):
    a="this is a response from appurlproject"
    return HttpResponse(a)