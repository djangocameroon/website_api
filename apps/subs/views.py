from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.subs.models import Subscriber
from apps.subs.serializers import (
    SendVerificationEmailSerializer,
    SubscriberSerializer,
    UnsubscribeSerializer,
    VerifySubscriptionTokenSerializer,
)
from apps.subs.services import SubscriberUnsubscribeService, SubscriptionVerificationService
from apps.subs.tasks import send_subscription_verification_email_task
from apps.users.serializers.general_serializers import ErrorResponseSerializer, SuccessResponseSerializer
from mixins.api_response_mixin import APIResponseMixin

# Create your views here.
@extend_schema_view(
    post=extend_schema(
        summary="Create subscriber",
        description="Create a new subscriber",
        tags=["Subscriber"],
    ),
)
class SubscriberCreateView(generics.CreateAPIView, APIResponseMixin):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Create subscriber",
        description="Create a new subscriber",
        tags=["Subscriber"],
        request=SubscriberSerializer,
        responses={
            201: OpenApiResponse(response=SubscriberSerializer, description=_("Subscriber created successfully")),
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
        if Subscriber.objects.filter(email=request.data.get('email')).exists():
            return self.success(
                message=_("This email is already subscribed."),
                status_code=status.HTTP_200_OK
            )
        return super().post(request, *args, **kwargs)


class SendSubscriptionVerificationView(APIResponseMixin, APIView):
    """Send (or resend) a subscription email-verification link to the given email."""
    serializer_class = SendVerificationEmailSerializer
    permission_classes = [permissions.AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "resend_verification"

    @extend_schema(
        operation_id="Send Subscription Verification Email",
        summary="Send subscription verification email",
        description="Emails a verification link for the given address. No Subscriber is created until the link is confirmed.",
        request=SendVerificationEmailSerializer,
        tags=["Subscriber"],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Verification email sent")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Bad request")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if Subscriber.objects.filter(email=email, is_verified=True).exists():
            return self.success(
                _("This email is already verified."),
                status_code=status.HTTP_200_OK
            )

        send_subscription_verification_email_task.delay(email)
        return self.success(
            _("Verification email sent."),
            status_code=status.HTTP_200_OK
        )


class VerifySubscriptionEmailView(APIResponseMixin, APIView):
    """Verify a subscription email using the token from the verification link."""
    serializer_class = VerifySubscriptionTokenSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="Verify Subscription Email",
        summary="Verify subscription email",
        description="Verifies the token from the subscription verification email and creates/activates the Subscriber.",
        request=VerifySubscriptionTokenSerializer,
        tags=["Subscriber"],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Email verified successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Invalid or expired token")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        email = SubscriptionVerificationService().verify_token(token)
        if not email:
            return self.error(
                _("Invalid or expired verification token."),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return self.success(
            _("Email verified successfully."),
            status_code=status.HTTP_200_OK
        )


class UnsubscribeView(APIResponseMixin, APIView):
    """Unsubscribe using the stable per-subscriber token (e.g. from an email footer link)."""
    serializer_class = UnsubscribeSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="Unsubscribe",
        summary="Unsubscribe",
        description="Removes the subscriber matching the given unsubscribe token.",
        request=UnsubscribeSerializer,
        tags=["Subscriber"],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_("Unsubscribed successfully")
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_("Invalid unsubscribe token")
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        email = SubscriberUnsubscribeService().unsubscribe(token)
        if not email:
            return self.error(
                _("Invalid unsubscribe token."),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return self.success(
            _("You have been unsubscribed successfully."),
            status_code=status.HTTP_200_OK
        )
