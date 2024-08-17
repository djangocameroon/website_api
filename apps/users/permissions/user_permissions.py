from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasPermission(BasePermission):
    """
    Custom permission class to check for specific permissions required by the view.
    """

    def has_permission(self, request, view):
        required_permissions = getattr(view, "required_permissions", [])
        exempt_methods = getattr(view, "exempt_methods", [])

        if not required_permissions:
            raise Exception(
                _("Required permissions not set in view. Please define 'required_permissions' attribute.")
            )

        if request.method in exempt_methods:
            return True

        if not request.user.is_authenticated:
            raise DRFPermissionDenied(_("Authentication credentials were not provided."))

        for permission in required_permissions:
            if not request.user.has_perm(permission):
                raise DRFPermissionDenied(
                    _("You do not have the required permission: '{permission}' to perform this action.").format(
                        permission=permission)
                )

        return True


class HasRole(BasePermission):
    """
    Custom permission class to check for specific roles required by the view.
    """

    def has_permission(self, request, view):
        required_roles = getattr(view, "required_roles", [])
        exempt_methods = getattr(view, "exempt_methods", [])

        if not required_roles:
            raise Exception(
                _("Required roles not set in view. Please define 'required_roles' attribute.")
            )

        if request.method in exempt_methods:
            return True

        if not request.user.is_authenticated:
            raise DRFPermissionDenied(_("Authentication credentials were not provided."))

        for role in required_roles:
            if not request.user.groups.filter(name=role).exists():
                raise DRFPermissionDenied(
                    _("You do not have the required role: '{role}' to perform this action.").format(role=role)
                )

        return True


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access for non-admin users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_superuser


class IsOrganizer(BasePermission):
    """
    Custom permission to check if the connected user is an organizer.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return False