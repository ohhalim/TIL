from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [  
    path('hello/',views.hello, name="hello"),
    path('data_throw/', views.data_throw, name ='data_throw'),
    path('data_catch/', views.data_catch, name ='data_catch'), 
]

 