
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProductPermission(BasePermission):

    def has_permission(self, request, view):

        user = request.user


        if not user or not user.is_authenticated:
            return False

        
        if request.method in SAFE_METHODS:
            return True

     
        if user.is_superuser:
            return True

        
        if user.is_staff and request.method in ['POST', 'PUT', 'PATCH']:
            return True

        return False
