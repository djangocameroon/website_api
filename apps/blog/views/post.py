from uuid import UUID

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.openapi import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.errors import BlogNotFoundErrorResponse
from apps.blog.models.blog import Blog
from apps.blog.serializers.blog_serializer import (
    BlogCreateUpdateResponseSerializer,
    BlogCreateUpdateSerializer,
    BlogLikeToggleResponseSerializer,
    BlogSerializer,
)
from apps.blog.services.blog_likes import BlogLikeService
from apps.blog.services.blog_views import BlogViewService
from apps.users.serializers.general_serializers import ErrorResponseSerializer
from mixins import APIResponseMixin


class PostList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogCreateUpdateSerializer
        return BlogSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @extend_schema(
        summary="List blog posts",
        description="Retrieve a list of blog posts",
        tags=["Blog"],
        responses={
            200: OpenApiResponse(response=BlogSerializer(many=True), description=_("List of blog posts retrieved successfully")),
            500: OpenApiResponse(response=ErrorResponseSerializer, description=_("Internal Server Error"))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create blog post",
        description="Create a new blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={
            201: OpenApiResponse(response=BlogCreateUpdateResponseSerializer, description=_("Blog post created successfully")),
            422: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Unprocessable Entity")
            ),
            500: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Internal Server Error")
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogCreateUpdateSerializer
        return BlogSerializer

    def get_object(self):
        lookup_field = self.kwargs.get('pk')
        query = Q(slug=lookup_field)
    
        try:
            UUID(lookup_field)
            query |= Q(id=lookup_field)
        except ValueError:
            pass

        try:
            obj = Blog.objects.get(query)
        except Blog.DoesNotExist:
            raise Http404
        return obj

    @extend_schema(
        summary="Get blog post",
        description="Retrieve a blog post",
        tags=["Blog"],
        responses={
            200: OpenApiResponse(
                response=BlogSerializer, 
                description=_("Blog post retrieved successfully")
            ),
            404: OpenApiResponse(
                response=BlogNotFoundErrorResponse,
                description=_("Blog post not found")
            ),
        },
        parameters=[
            OpenApiParameter(
                    name='id',
                    location=OpenApiParameter.PATH,
                    description='id or slug of the blog post',
                    required=True,
                    type=OpenApiTypes.STR,
                )
            ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update blog post",
        description="Update a blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={200: BlogCreateUpdateResponseSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update blog post",
        description="Partially update a blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={200: BlogCreateUpdateResponseSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete blog post",
        description="Delete a blog post",
        tags=["Blog"],
        responses={
            204: OpenApiResponse(
                response=None,
                description=_("Blog post deleted successfully")
            ),
            403: OpenApiResponse(
                response=None,
                description=_("Forbidden: You do not have permission to delete this blog post")
            ),
            404: OpenApiResponse(
                response=None,
                description=_("Not Found: Blog post does not exist")
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        if request.user.username != self.get_object().author.username:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        BlogViewService.track(request, blog)
        return super().get(request, *args, **kwargs)

class PostLikeToggleView(APIResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    @extend_schema(
        summary="Toggle blog post like",
        description="Like the blog post if the user hasn't liked it yet, otherwise unlike it.",
        tags=["Blog"],
        request=None,
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id of the blog post',
                required=True,
                type=OpenApiTypes.UUID,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=BlogLikeToggleResponseSerializer,
                description=_("Blog like toggled successfully"),
            ),
            404: OpenApiResponse(
                response=BlogNotFoundErrorResponse,
                description=_("Blog post not found"),
            ),
        },
    )
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        result = BlogLikeService.toggle(blog, request.user)
        return self.success(
            _("Blog like toggled successfully"),
            result,
            status.HTTP_200_OK   
        )