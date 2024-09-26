from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAuthorOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an author to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow unauthenticated users to view authors (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # For non-safe methods (POST, PUT, DELETE), ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are always allowed
        if request.method in SAFE_METHODS:
            return True
        # Only the author owner can edit or delete the author
        return obj.user == request.user  # Assuming you have a `user` field in your Author model
