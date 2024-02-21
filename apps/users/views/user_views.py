from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework import status
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from mixins import APIResponseMixin
from apps.users.serializers import UserSerializer, SuccessResponseSerializer, ErrorResponseSerializer

User = get_user_model()

# Get user details view
class UserDetails(APIResponseMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_id="Get user details",
        operation_summary="Get user details",
        tags=["User"],
        responses={
            200: UserSerializer,
            400: ErrorResponseSerializer,
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return self.success(
            message=_('User details retrieved successfully'),
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

class UpdateUserProfile(APIResponseMixin, UpdateModelMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_id="Update user profile",
        operation_summary="Update user profile",
        tags=["User"],
        request_body=UserSerializer,
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        }
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return self.success(
            message=_('User profile updated successfully'),
            status=status.HTTP_200_OK,
            data=serializer.data,
        )   
