
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProductPermission(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        # Only authenticated users
        if not user or not user.is_authenticated:
            return False

        # Everyone authenticated can view
        if request.method in SAFE_METHODS:
            return True

        # Admin can perform all operations
        if user.is_superuser:
            return True

        # Staff can create and update
        if user.is_staff and request.method in ['POST', 'PUT', 'PATCH']:
            return True

        return False
