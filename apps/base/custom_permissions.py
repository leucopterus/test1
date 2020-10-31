from rest_framework.permissions import BasePermission


class IsOrganizerOrParticapatorOrAdmin(BasePermission):
    """Access have only organizer, participators and superuser"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and bool(
            request.user.is_superuser or
            request.user in obj.participators.all()
            or request.user.id == obj.organizer.id
        )
