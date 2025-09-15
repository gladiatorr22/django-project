from django.contrib import admin

# Register your models here.
from myapp.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display=['number','name','marks']
admin.site.register(Student,StudentAdmin)
