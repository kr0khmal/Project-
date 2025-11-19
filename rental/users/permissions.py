from rest_framework.permissions import BasePermission


class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "tenant"


class IsLandlord(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "landlord"
