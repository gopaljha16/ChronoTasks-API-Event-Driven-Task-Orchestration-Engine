from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission check for admin users only
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission check for object owner or admin
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.created_by == request.user if hasattr(obj, 'created_by') else False
