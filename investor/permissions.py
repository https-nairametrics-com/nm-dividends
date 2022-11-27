from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsUserApproved(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.investor.is_approved == True
