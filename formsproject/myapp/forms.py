from django import forms

class studentForm(forms.Form):
    name=forms.CharField()
    age=forms.IntegerField()
    place=forms.CharField()
    email=forms.EmailField()
    dob=forms.DateField(input_formats=['%d-%m-%Y'])

