from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view2(request):
    b="this is a response from second app"
    return HttpResponse(b)