"""
Custom exception handler for standardized API error responses.

This module provides a custom exception handler that intercepts DRF exceptions
and formats them using the standardized response envelope with proper error codes.
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    Throttled,
)
from rest_framework import status

from .responses import error_response
from .error_codes import ErrorCode


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats DRF exceptions into standardized responses.

    This handler maps common DRF exceptions to appropriate error codes and formats
    the response using the standardized error_response() utility.

    Args:
        exc: The exception that was raised
        context: Dictionary containing request and view information

    Returns:
        Standardized Response object with error details
    """
    # First, let DRF handle the exception to get the standard response
    response = exception_handler(exc, context)

    if response is not None:
        # Map DRF exceptions to our error codes
        error_code, details = _map_exception_to_error_code(exc, response)

        # Return standardized error response
        return error_response(
            error_code=error_code,
            details=details,
            status_code=response.status_code,
        )

    # If DRF didn't handle it, it's an unhandled exception
    # Return a generic internal error response
    return error_response(
        error_code=ErrorCode.INTERNAL_ERROR,
        details="An unexpected error occurred. Please try again later.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _map_exception_to_error_code(exc, response):
    """
    Map DRF exceptions to application error codes.

    Args:
        exc: The exception that was raised
        response: The DRF response object

    Returns:
        Tuple of (ErrorCode, details)
    """
    # Default error code and details
    error_code = ErrorCode.INTERNAL_ERROR
    details = None

    # Extract error details from response data
    if hasattr(response, 'data'):
        if isinstance(response.data, dict):
            # Handle field-level validation errors
            if 'detail' in response.data:
                details = response.data['detail']
            else:
                details = response.data
        elif isinstance(response.data, list):
            details = response.data[0] if response.data else None
        else:
            details = str(response.data)

    # Map exception types to error codes
    if isinstance(exc, AuthenticationFailed):
        error_code = ErrorCode.AUTHENTICATION_FAILED
        if 'detail' in exc.detail if hasattr(exc, 'detail') else False:
            auth_detail = str(exc.detail.get('detail', str(exc.detail)))
            if 'expired' in auth_detail.lower():
                error_code = ErrorCode.EXPIRED_TOKEN
            elif 'invalid' in auth_detail.lower() or 'token' in auth_detail.lower():
                error_code = ErrorCode.INVALID_TOKEN

    elif isinstance(exc, NotAuthenticated):
        error_code = ErrorCode.NOT_AUTHENTICATED

    elif isinstance(exc, ValidationError):
        error_code = ErrorCode.VALIDATION_ERROR
        # Keep field-level validation details
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            details = exc.detail

    elif isinstance(exc, PermissionDenied):
        error_code = ErrorCode.PERMISSION_DENIED

    elif isinstance(exc, NotFound):
        error_code = ErrorCode.NOT_FOUND
        if details is None and hasattr(exc, 'detail'):
            details = str(exc.detail)

    elif isinstance(exc, MethodNotAllowed):
        error_code = ErrorCode.PERMISSION_DENIED
        details = f"Method {context['request'].method} not allowed."

    elif isinstance(exc, Throttled):
        error_code = ErrorCode.SERVICE_UNAVAILABLE
        if hasattr(exc, 'detail'):
            details = str(exc.detail)

    return error_code, details


def handle_jwt_error(error_message):
    """
    Handle JWT-specific errors and return appropriate error code.

    Args:
        error_message: The error message from JWT processing

    Returns:
        ErrorCode enum value
    """
    error_lower = error_message.lower()

    if 'expired' in error_lower:
        return ErrorCode.EXPIRED_TOKEN
    elif 'invalid' in error_lower or 'signature' in error_lower:
        return ErrorCode.INVALID_TOKEN
    elif 'blacklist' in error_lower:
        return ErrorCode.TOKEN_BLACKLISTED
    else:
        return ErrorCode.AUTHENTICATION_FAILED
