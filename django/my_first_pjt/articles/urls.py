from django.urls import path
from . import views


urlpatterns = [  
    path('', views.articles, name="articles"),
    path("new/", views.new, name="new"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.article_detail, name="article_detail"),
    
    path("index/", views.index, name="index"),
    path('data_throw/', views.data_throw, name ='data_throw'),
    path('data_catch/', views.data_catch, name ='data_catch'), 
]

