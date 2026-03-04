from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth import get_user_model
from django.db.models import Count
from apps.blog.serializers.author_serializer import AuthorSerializer

User = get_user_model()

@extend_schema_view(
    get=extend_schema(
        summary="List authors",
        description="Retrieve a list of blog authors with more than one blog post",
        tags=["Blog - Authors"],
    )
)
class AuthorListView(generics.ListAPIView):
    queryset = User.objects.annotate(blog_count=Count('blog')).filter(blog_count__gt=1)
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
