from rest_framework import generics, permissions
from apps.blog.models.blog import Blog
from apps.blog.serializers.blog_serializer import BlogSerializer, BlogCreateUpdateSerializer


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
