from django.urls import path
from apps.blog.views import post
from apps.blog.views.post import (PostCreateView, PostDetailView, PostListView, UserProfileListView)

urlpatterns = [
    path('creat-posts/', PostCreateView.as_view(), name = 'create-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('posts', PostListView.as_view, name = 'posts'),
    path('user/posts/', UserProfileListView.as_view(), name = 'user-posts'),
    
    
]