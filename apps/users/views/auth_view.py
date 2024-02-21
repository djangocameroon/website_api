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
from apps.users.models import OtpCode
import secrets
from django.contrib.contenttypes.models import ContentType
from apps.users.serializers import (
    UserRegistrationSerializer, SuccessResponseSerializer, 
    ErrorResponseSerializer, LoginSerializer,
    LoginResponseSerializer, UserSerializer,
    PassWordResetRequestSerializer, PasswordResetConfirmationSerializer
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
      

        application, created = Application.objects.get_or_create(name="Default")
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
    

class PasswordResetRequestView(APIResponseMixin, APIView):
    serializer_class = PassWordResetRequestSerializer
    permission_classes = [ permissions.AllowAny ]
    
    @swagger_auto_schema(
        operation_id="Reset Password",
        operation_summary="Reset Password",
        request_body=PassWordResetRequestSerializer,
        tags=['Auth'],
        security=[],
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        },
    ) 
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']

        # Check if the user with the provided email exists or not
        user = User.objects.filter(email=email).first()
        if user is None:
            return self.error(_("User with the provided email does not exist"), status.HTTP_400_BAD_REQUEST)
        
        user.send_email_otp()

        return self.success(_("An OTP has been sent to your email for verification"), status.HTTP_200_OK)
    

class PasswordResetConfirmationView(APIResponseMixin, APIView):
    serializer_class = PasswordResetConfirmationSerializer
    permission_classes = [ permissions.AllowAny ]
    
    @swagger_auto_schema(
        operation_id="Reset Password Confirmation",
        operation_summary="Reset Password Confirmation",
        request_body=PasswordResetConfirmationSerializer,
        tags=['Auth'],
        security=[],
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        },
    ) 
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        otp = data['otp']
        password = data['password']
        
        user_content_type = ContentType.objects.get_for_model(User)
        otp_model = OtpCode.objects.filter(
            otp_code=otp,
            content_type=user_content_type
        ).first()
        if otp_model is None:
            return self.error(_("Invalid OTP"), status.HTTP_400_BAD_REQUEST)
        
        # Check if it has expired and delete if that its the case
        if otp_model.has_expired():
            otp_model.delete()
            return self.error(_("OTP has expired. Make a new request"), status.HTTP_400_BAD_REQUEST)
        
        user = otp_model.content_object
        
        if user is None:
            return self.error(_("Invalid OTP"), status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()

        otp_model.delete()

        # delete all the user's access tokens
        AccessToken.objects.filter(user=user).delete()
        
        return self.success(_("Password reset successfully"), status.HTTP_200_OK)
    
class LogoutView(APIResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_id="Logout",
        operation_summary="Logout",
        tags=['Auth'],
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        },
    ) 
    def post(self, request, *args, **kwargs):
        user = request.user
        AccessToken.objects.filter(user=user).delete()
        return self.success(_("Logout successfull"), status.HTTP_200_OK)
    