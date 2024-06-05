from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """ Разрешение проверяет, является ли пользователь модератором """
    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()
