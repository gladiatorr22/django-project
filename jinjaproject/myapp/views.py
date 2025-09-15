from django.shortcuts import render

# Create your views here.
def view1(request):
    name="rama"
    place="bangalore"
    ctx={'NAME':name,'PLACE':place}
    return render(request,'myapp/1.html',ctx)

