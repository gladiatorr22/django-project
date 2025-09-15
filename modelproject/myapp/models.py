from django.db import models

# Create your models here.
class Student(models.Model):
    number=models.IntegerField()
    name=models.CharField(max_length=40)
    marks=models.FloatField()
    
def __str__(self):
    return self.name

    