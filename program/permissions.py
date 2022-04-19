from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)
