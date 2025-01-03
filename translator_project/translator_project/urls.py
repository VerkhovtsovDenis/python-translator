from django.contrib import admin
from django.urls import include, path
from . import vievs

urlpatterns = [
    path('', include('main.urls'), name='main'),
    
]
