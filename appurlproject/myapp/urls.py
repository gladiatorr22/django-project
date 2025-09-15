from django.urls import path
from myapp.views import view1

urlpatterns=[
    path('r1/',view1),
]