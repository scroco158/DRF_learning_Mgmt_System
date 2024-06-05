from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """ Разрешение проверяет, является ли пользователь модератором """
    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    """ Проверяет, является ли пользователь владельцем. """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

