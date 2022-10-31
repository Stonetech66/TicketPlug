from rest_framework.permissions import BasePermission, SAFE_METHODS

# class IsSuper(BasePermission):
#     def has_object_permission(self, request, obj, view):
#         if request.method in permissions.SAFE_METHOD:
#             return True
#         return request.user.is_superuser 

class IsAdminorReadOnly(BasePermission):
    def has_permission(self, request, view ):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user



