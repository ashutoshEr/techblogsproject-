from django.urls import path, include
from django.contrib import admin
from . import views 

urlpatterns = [   
   # api to post a comment 
    path('', views.blogHome, name='blogHome'),  
    path('postcomment', views.postcomment, name = "postcomment"),
    path('profile', views.profile, name = 'profile'),
    path('profileNewPost', views.profileNewPost, name = 'profileNewPost'),
    path('profileRecentPost', views.profileRecentPost, name = 'profileRecentPost'),
    path('profileStats', views.profileStats, name = 'profileStats'),
    
    path('<str:slug>', views.blogPost, name='blogPost'),  
]
