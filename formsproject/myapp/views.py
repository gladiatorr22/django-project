from django.shortcuts import render
from myapp.forms import studentForm
# Create your views here.
def formview(request):
    f=studentForm()
    if request.method== 'POST':
        f=  studentForm(request.POST)
        if f.is_valid():
            name=f.cleaned_data['name']
            age=f.cleaned_data['age']
            place = f.cleaned_data['place']
            email = f.cleaned_data['email']
            dob = f.cleaned_data['dob']
            d={'name':name,'age':age,'place':place,'email':email,'dob':dob}
            return render(request,'myapp/output.html',d)
    else:  # This else block is the key to fixing the ValueError
        f = studentForm()
        
    d={'form':f}
    return render(request,'myapp/input.html',d)



