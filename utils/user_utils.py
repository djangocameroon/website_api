from oauth2_provider.models import AccessToken, RefreshToken


def get_connected_user(request):
    token = request.headers.get("Authorization", None)
    if token:
        try:
            existing_access_token = AccessToken.objects.get(token=token)
            connected_user = existing_access_token.user
        except:
            existing_refresh_token = RefreshToken.objects.get(token=token)
            connected_user = existing_refresh_token.user
        return connected_user
    return None
