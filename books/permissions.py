from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsBookOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a book to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow unauthenticated users to view books (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # For non-safe methods (POST, PUT, DELETE), ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are always allowed
        if request.method in SAFE_METHODS:
            return True
        # Only the book owner can edit or delete the book
        return obj.user == request.user
