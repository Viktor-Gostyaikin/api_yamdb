from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadOrAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        def check_role(request, *args):
            if request.user.is_authenticated:
                if request.user.role in args:
                    return True
                elif request.user.is_superuser:
                    return True
            return False
        return (request.method in permissions.SAFE_METHODS
                or check_role(request, User.ADMIN))


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        def check_role(request, *args):
            if request.user.is_authenticated:
                if request.user.role in args:
                    return True
                elif request.user.is_superuser:
                    return True
            return False
        return (check_role(request, User.ADMIN))


class AuthorOrAdminOrModeratorOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated
                and (request.user.role == User.ADMIN
                     or request.user.role == User.MODERATOR
                     or obj.author == request.user))
