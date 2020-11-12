from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'Ты должен быть \'Администратором\' сорри.'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSpecialist(BasePermission):
    message = 'Ты должен быть \'Специалистом\' сорри.'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_spec)

class SelfOrAdmin(BasePermission):
    message = 'Это не твой аккаунт или ты не \'Администратор\'.'
    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user == obj or request.user.is_superuser == True))