from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from mixins import APIResponseMixin
from apps.users.serializers import UserRegistrationSerializer, SuccessResponseSerializer, ErrorResponseSerializer

class UserRegistrationView(APIView, APIResponseMixin):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_id="Register user",
        operation_summary="Register user",
        request_body=UserRegistrationSerializer,
        tags=["Auth"],
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return self.success(
            message=_('User account created successfully'),
            status=status.HTTP_201_CREATED,
            data=serializer.data,
        )