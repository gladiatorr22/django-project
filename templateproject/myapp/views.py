from django.shortcuts import render

# Create your views here.
def view1(request):
    return render(request,'myapp/1.html')

def view2(request):
    return render(request,'myapp/2.html')