from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanManageCatalog(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_staff


class CanManageEvent(BasePermission):
    def has_object_permission(self, request, view, event):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or event.submitted_by_id == request.user.pk
        )
