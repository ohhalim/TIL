from django.urls import path
from. import views

 
urlpatterns = [  
    path('hello/',views.hello),
    path('data-throw/',views.data_throw),
    path('data-catch/',views.data_catch), 
]