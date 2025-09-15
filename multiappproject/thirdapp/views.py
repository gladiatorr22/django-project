from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view3(request):
    c="this is a response from third app"
    return HttpResponse(c)