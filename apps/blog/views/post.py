from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework import permissions

from apps.blog.models.post import Category, Tag, Post
from apps.blog.serializers.post_serializer import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    
class UserProfileListView(generics.ListAPIView):   #Lists all posts by a specific user
    serializer_class = PostSerializer
    pagination_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    