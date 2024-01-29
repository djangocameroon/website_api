from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.timezone import now, timedelta
from drf_yasg.utils import swagger_auto_schema
from mixins import APIResponseMixin
from oauth2_provider.models import AccessToken, RefreshToken, Application
import secrets
from apps.users.serializers import (
    UserRegistrationSerializer, SuccessResponseSerializer, 
    ErrorResponseSerializer, LoginSerializer,
    LoginResponseSerializer, UserSerializer
)

User = get_user_model()

class UserRegistrationView(APIResponseMixin, APIView):
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
    
    
class LoginView(APIResponseMixin, APIView):
    serializer_class = LoginSerializer
    permission_classes = [ permissions.AllowAny ]
    
    @swagger_auto_schema(
        operation_id="Login",
        operation_summary="Login a user",
        request_body=LoginSerializer,
        tags=['Auth'],
        security=[],
        responses={
            200: LoginResponseSerializer,
        },
    ) 
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        # Check if the data['email_or_phone'] is not
        email_or_phone = data['email_or_username']
        is_mail = email_or_phone.find('@') != -1
        
        if is_mail:
            user = authenticate(email=email_or_phone, password=data['password'])
        else:
            ruser = User.objects.filter(username=email_or_phone).first()
            if ruser is not None:
                user = authenticate(email=ruser.email, password=data['password'])
            else:
                user = None

        if user is None:
            return self.error(_("Invalid credentials"), status.HTTP_400_BAD_REQUEST)
      

        application = Application.objects.get(name="Default")
        expiration_time = now() + timedelta(days=1)

        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            expires=expiration_time,
            token=secrets.token_hex(16),
        )
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=secrets.token_hex(16),
        )
        refresh_token.access_token = access_token
        refresh_token.save()

        response_data = {
            "access_token": access_token.token,
            "refresh_token": refresh_token.token,
            "expires_in": access_token.expires,
            "user": UserSerializer(user).data,
        }
        
        return self.success(_("Login successfull"), status.HTTP_200_OK, response_data)
