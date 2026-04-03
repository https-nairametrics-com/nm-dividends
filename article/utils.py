from rest_framework.response import Response


def success_response(message, data=None, status_code=200, meta=None):
    """
    Standard success response format
    """
    payload = {
        "success": True,
        "message": message,
        "data": data
    }

    if meta is not None:
        payload["meta"] = meta

    return Response(payload, status=status_code)


def error_response(message, error, details=None, status_code=400):
    """
    Standard error response format
    """
    payload = {
        "success": False,
        "message": message,
        "error": error,
        "details": details or {}
    }

    return Response(payload, status=status_code)


def get_user_role(user):
    """
    Determine user role using Django's built-in permissions.

    superuser -> admin
    staff -> editor
    authenticated -> user
    anonymous -> None
    """

    if not user or not user.is_authenticated:
        return None

    if user.is_superuser:
        return "admin"

    if user.is_staff:
        return "editor"

    return "user"


def is_admin(user):
    """
    Check if user is admin
    """
    return get_user_role(user) == "admin"


def is_editor(user):
    """
    Check if user is editor
    """
    return get_user_role(user) == "editor"


def is_admin_or_editor(user):
    """
    Check if user has content management rights
    """
    role = get_user_role(user)
    return role in ["admin", "editor"]