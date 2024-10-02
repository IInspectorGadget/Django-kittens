from rest_framework import permissions
from rest_framework.exceptions import ValidationError


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class CanRateOthersKittens(permissions.BasePermission):
    """
    Разрешение на оценку котят только для тех, которые не принадлежат пользователю.
    """
    def has_permission(self, request, view):
        return request.method in ['POST', 'PUT', 'DELETE', 'PATCH', 'GET']

    def has_object_permission(self, request, view, obj):
        print(obj.kitten.owner, request.user)
        if obj.kitten.owner == request.user:
            raise ValidationError("Вы не можете оценивать своих котят.")
        return True