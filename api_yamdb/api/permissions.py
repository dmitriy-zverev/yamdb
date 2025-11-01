from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ReadOnlyOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or not request.user.is_anonymous and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return not request.user.is_anonymous and request.user.is_admin
