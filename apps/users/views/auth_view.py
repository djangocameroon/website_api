from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from oauth2_provider.models import AccessToken
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from apps.users.helpers.auth import generate_tokens, get_serializer
from apps.users.models import OtpCode
from apps.users.serializers import (
    UserRegistrationSerializer, SuccessResponseSerializer,
    ErrorResponseSerializer, LoginSerializer,
    LoginResponseSerializer, UserSerializer,
    PassWordResetRequestSerializer, PasswordResetConfirmationSerializer,
    EmailVerificationSerializer
)
from mixins import APIResponseMixin
from utils.auth import authenticate_user

User = get_user_model()


class UserRegistrationView(APIResponseMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Register user",
        summary="Register user",
        request=UserRegistrationSerializer,
        tags=["Auth"],
        responses={
            201: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("User account created successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Bad request")
            ),
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return self.success(
            message=_('User account created successfully'),
            status_code=status.HTTP_201_CREATED,
            data={}
        )


class LoginView(APIResponseMixin, APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Login",
        summary="Login a user",
        request=LoginSerializer,
        tags=['Auth'],
        responses={
            200: OpenApiResponse(response=LoginResponseSerializer, description=_("Login successfully")),
            400: OpenApiResponse(response=ErrorResponseSerializer, description=_("Invalid credentials")),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = get_serializer(self, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate_user(self, serializer.validated_data)

        if not user:
            return self.error(
                _("Invalid credentials"),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        tokens = generate_tokens(self, user)
        response_data = {
            "access_token": tokens['access_token'].token,
            "refresh_token": tokens['refresh_token'].token,
            "expires_in": tokens['access_token'].expires,
            "user": UserSerializer(user).data,
        }

        return self.success(_("Login successfully"), response_data, status.HTTP_200_OK)


class PasswordResetRequestView(APIResponseMixin, APIView):
    serializer_class = PassWordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Reset Password",
        summary="Reset Password",
        request=PassWordResetRequestSerializer,
        tags=['Auth'],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("An OTP has been sent to your email for verification")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("User with the provided email does not exist")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            return self.error(
                _("User with the provided email does not exist"),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user.send_email_otp()
        return self.success(
            _("An OTP has been sent to your email for verification"),
            status_code=status.HTTP_200_OK,
        )


class PasswordResetConfirmationView(APIResponseMixin, APIView):
    serializer_class = PasswordResetConfirmationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Reset Password Confirmation",
        summary="Reset Password Confirmation",
        request=PasswordResetConfirmationSerializer,
        tags=['Auth'],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Password reset successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Invalid OTP or expired OTP")
            ),
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

        if otp_model.has_expired():
            otp_model.delete()
            return self.error(
                _("OTP has expired. Make a new request"),
                status.HTTP_400_BAD_REQUEST
            )
        user = otp_model.content_object

        if user is None:
            return self.error(_("Invalid OTP"), status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        otp_model.delete()
        AccessToken.objects.filter(user=user).delete()

        return self.success(
            _("Password reset successfully"),
            status.HTTP_200_OK
        )


class LogoutView(APIResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Logout",
        summary="Logout",
        tags=['Auth'],
        responses={
            205: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Logout successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Error during logout")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        AccessToken.objects.filter(user=user).delete()
        return self.success(
            _("Logout successfully"),
            status.HTTP_205_RESET_CONTENT
        )


class EmailVerificationView(APIResponseMixin, APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="Verify Email",
        summary="Verify email with OTP and activate account",
        request=EmailVerificationSerializer,
        tags=['Auth'],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Email verified successfully. Your account is now active.")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Invalid or expired OTP")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']

        user = User.objects.filter(email=email).first()
        if not user:
            return self.error(
                _("User with this email does not exist"),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active:
            return self.error(
                _("Account is already active"),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user_content_type = ContentType.objects.get_for_model(User)
        otp_model = OtpCode.objects.filter(
            otp_code=otp_code,
            content_type=user_content_type,
            object_id=user.pk
        ).first()

        if not otp_model:
            return self.error(
                _("Invalid OTP code"),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if otp_model.has_expired():
            otp_model.delete()
            return self.error(
                _("OTP has expired. Please request a new one."),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.save(update_fields=['is_active'])
        otp_model.delete()

        return self.success(
            _("Email verified successfully. Your account is now active."),
            status_code=status.HTTP_200_OK
        )
