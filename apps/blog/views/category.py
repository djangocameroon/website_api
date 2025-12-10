from rest_framework import generics
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.blog.models.category import Category
from apps.blog.serializers.category_serializer import CategorySerializer


@extend_schema_view(
    get=extend_schema(
        summary="List categories",
        description="Retrieve a list of blog categories",
        tags=["Blog - Categories"],
    ),
    post=extend_schema(
        summary="Create category",
        description="Create a new blog category",
        tags=["Blog - Categories"],
    ),
)
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
