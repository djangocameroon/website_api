from rest_framework import generics
from apps.blog.models.category import Category
from apps.blog.serializers.category_serializer import CategorySerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
