from django.urls import path
from. import views

urlpatterns = [
    path('',views.users),
    path('profile/<str:username>/', views.profile),
]
