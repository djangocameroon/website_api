from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, SuccessResponseSerializer, ErrorResponseSerializer
from mixins import APIResponseMixin

User = get_user_model()


class UserDetails(APIResponseMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Get user details",
        summary="Get user details",
        tags=["User"],
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description=_("User details retrieved successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Bad request")
            ),
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return self.success(
            message=_('User details retrieved successfully'),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )


class UpdateUserProfile(APIResponseMixin, UpdateModelMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Update user profile",
        summary="Update user profile",
        tags=["User"],
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("User profile updated successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Bad request")
            ),
        }
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.success(
            message=_('User profile updated successfully'),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )
