from django.shortcuts import render

# Create your views here.
def myview(request):
    name="rama"
    animal="dog"
    bird="peacock"
    color="black"
    ctx={'Name':name,'Animal':animal,'Bird':bird,'Color':color}
    return render(request,'myapp/1.html',ctx)