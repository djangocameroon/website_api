from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework.permissions import IsAdminUser


class IsOrganizer(IsAdminUser):
    """Check if the connected user is an organizer."""

    def has_permission(self, request, view):
        token = request.headers.get("Authorization", None)
        if token:
            try:
                existing_access_token = AccessToken.objects.get(token=token)
                connected_user = existing_access_token.user
            except:
                existing_refresh_token = RefreshToken.objects.get(token=token)
                connected_user = existing_refresh_token.user

            if connected_user.is_staff or connected_user.is_superuser:
                return True

        return False
