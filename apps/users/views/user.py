from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers.user import UserRegistrationSerializer, UserSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="Retrieve a list of all users",
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve details of a specific user",
        tags=["Users"],
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account",
        tags=["Users"],
        request=UserRegistrationSerializer,
        responses={201: UserSerializer},
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Get current user",
        description="Retrieve the currently authenticated user's details",
        tags=["Users"],
        responses={200: UserSerializer},
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
