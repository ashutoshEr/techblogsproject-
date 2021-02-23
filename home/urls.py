from django.contrib import admin
from django.urls import path, include
from home import views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('about', views.about, name='about'), 
    path('contact', views.contacts, name='contact'), 
    path('search', views.search, name='search'), 
    path('signup', views.Signup, name='Signup'), 
    path('login', views.Login, name='Login'),  
    path('logout', views.Logout, name='Logout'), 
]