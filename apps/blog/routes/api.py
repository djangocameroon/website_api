from django.urls import path
from apps.blog.views import post
from apps.blog.views.post import (PostCreateView)

urlpatterns = [
    path('posts/', PostCreateView.as_view(), name = 'create_post'),
    
]