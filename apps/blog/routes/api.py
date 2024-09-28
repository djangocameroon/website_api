from django.urls import path
from apps.blog.views.post import PostDetail,PostList
from apps.blog.views.blog import BlogListCreateView

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/create/', BlogListCreateView.as_view(), name='post-create'),
]
