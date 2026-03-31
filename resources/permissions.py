"""
Custom permissions for the resources app.
"""

from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """Permission that only allows read operations."""
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrEditor(permissions.BasePermission):
    """
    Permission that allows access to admin users or users with editor role.
    
    Editors are determined by checking is_staff flag.
    """
    
    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin or staff can edit
        return request.user.is_staff or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can do anything
        if request.user.is_superuser:
            return True
        
        # Staff can edit
        if request.user.is_staff:
            return True
        
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows access to the owner of the object or admin users.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_superuser:
            return True
        
        # Check if object has an owner field
        if hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        
        if hasattr(obj, 'author_user'):
            return obj.author_user == request.user
        
        return False
