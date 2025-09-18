from django.shortcuts import render

# Create your views here.
from myapp.models import Student
def view1(request):
    s=Student.objects.all()
    d={"Stud":s}
    return render(request,'myapp/1.html',d)

