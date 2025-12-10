from django.urls import path
from apps.blog.views.post import PostDetail, PostList
from apps.blog.views.blog import BlogListCreateView
from apps.blog.views.author import AuthorListView
from apps.blog.views.category import CategoryListView
from apps.blog.views.image import ImageListView, ImageCreateView
from apps.blog.views.tag import TagListView
from apps.blog.views.index import index


urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/create/', BlogListCreateView.as_view(), name='post-create'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('images/create/', ImageCreateView.as_view(), name='image-create'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('', index, name='index'),
]
