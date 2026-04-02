"""
Standardized API response utilities.

This module provides helper functions for creating consistent API responses
with proper structure, metadata, and user-friendly messages.
"""

from typing import Any, Optional, Dict, List, Union
from rest_framework.response import Response
from rest_framework import status as http_status
from .error_codes import ErrorCode, get_error_info


def api_response(
    success: bool = True,
    message: str = "",
    data: Optional[Any] = None,
    meta: Optional[Dict] = None,
    error: Optional[Dict] = None,
    status_code: int = http_status.HTTP_200_OK,
    headers: Optional[Dict] = None,
) -> Response:
    """
    Create a standardized API response.

    This helper ensures all API responses follow a consistent structure:
    {
        "success": bool,
        "message": str,
        "data": Any (optional),
        "meta": dict (optional, for paginated responses),
        "error": dict (optional, for error responses)
    }

    Args:
        success: Whether the request was successful
        message: User-friendly message describing the result
        data: Response data (for successful requests)
        meta: Metadata for paginated responses (page, per_page, total, etc.)
        error: Error details (for failed requests)
        status_code: HTTP status code
        headers: Optional HTTP headers

    Returns:
        DRF Response object with standardized format

    Examples:
        # Success response with data
        return api_response(
            success=True,
            message="User created successfully",
            data={"id": 1, "email": "user@example.com"},
            status_code=201
        )

        # Paginated list response
        return api_response(
            success=True,
            message="Resources retrieved",
            data=[...],
            meta={"current_page": 1, "per_page": 10, "total": 50}
        )

        # Error response
        return api_response(
            success=False,
            message="Authentication failed",
            error={
                "code": "AUTHENTICATION_FAILED",
                "details": "Invalid credentials",
                "help": "Please check your email and password"
            },
            status_code=401
        )
    """
    response_data = {
        "success": success,
        "message": message,
    }

    if data is not None:
        response_data["data"] = data

    if meta is not None:
        response_data["meta"] = meta

    if error is not None:
        response_data["error"] = error

    return Response(response_data, status=status_code, headers=headers)


def success_response(
    data: Any,
    message: str = "Success",
    meta: Optional[Dict] = None,
    status_code: int = http_status.HTTP_200_OK,
    headers: Optional[Dict] = None,
) -> Response:
    """
    Create a standardized success response.

    Args:
        data: Response data
        message: Success message
        meta: Optional pagination metadata
        status_code: HTTP status code (default: 200)
        headers: Optional HTTP headers

    Returns:
        DRF Response object

    Examples:
        # Single object
        return success_response(
            data={"id": 1, "name": "Resource"},
            message="Resource retrieved successfully"
        )

        # Created resource
        return success_response(
            data={"id": 1, "name": "Resource"},
            message="Resource created successfully",
            status_code=201
        )
    """
    return api_response(
        success=True,
        message=message,
        data=data,
        meta=meta,
        status_code=status_code,
        headers=headers,
    )


def error_response(
    error_code: ErrorCode,
    details: Optional[Union[str, Dict]] = None,
    status_code: Optional[int] = None,
    headers: Optional[Dict] = None,
) -> Response:
    """
    Create a standardized error response with user-friendly messages.

    Args:
        error_code: ErrorCode enum value
        details: Additional error details (string or field-level dict)
        status_code: HTTP status code (auto-detected from error_code if not provided)
        headers: Optional HTTP headers

    Returns:
        DRF Response object with standardized error format

    Examples:
        # Simple error
        return error_response(
            error_code=ErrorCode.NOT_FOUND,
            details="Resource with slug 'abc' does not exist"
        )

        # Validation error with field details
        return error_response(
            error_code=ErrorCode.VALIDATION_ERROR,
            details={"email": ["This field is required"]}
        )

        # Authentication error
        return error_response(ErrorCode.AUTHENTICATION_FAILED)
    """
    error_info = get_error_info(error_code)

    # Use provided status code or get from error code mapping
    if status_code is None:
        status_code = error_info["status"]

    # Build error object
    error_obj = {
        "code": error_info["code"],
        "details": details if details is not None else error_info["message"],
        "help": error_info["help"],
    }

    return api_response(
        success=False,
        message=error_info["message"],
        error=error_obj,
        status_code=status_code,
        headers=headers,
    )


def paginated_response(
    data: List[Any],
    page: int,
    per_page: int,
    total: int,
    message: str = "Data retrieved successfully",
) -> Response:
    """
    Create a standardized paginated response.

    Args:
        data: List of items for current page
        page: Current page number (1-indexed)
        per_page: Items per page
        total: Total number of items
        message: Success message

    Returns:
        DRF Response object with pagination metadata

    Example:
        return paginated_response(
            data=serializer.data,
            page=page,
            per_page=per_page,
            total=queryset.count()
        )
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    meta = {
        "current_page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }

    return success_response(
        data=data,
        message=message,
        meta=meta,
    )


def created_response(
    data: Any,
    message: str = "Resource created successfully",
    headers: Optional[Dict] = None,
) -> Response:
    """
    Create a standardized resource creation response.

    Args:
        data: Created resource data
        message: Success message
        headers: Optional HTTP headers (e.g., Location)

    Returns:
        DRF Response object with 201 status
    """
    return success_response(
        data=data,
        message=message,
        status_code=http_status.HTTP_201_CREATED,
        headers=headers,
    )


def deleted_response(
    message: str = "Resource deleted successfully",
) -> Response:
    """
    Create a standardized resource deletion response.

    Args:
        message: Success message

    Returns:
        DRF Response object
    """
    return success_response(
        data=None,
        message=message,
    )


def validation_error_response(
    field_errors: Dict[str, List[str]],
    message: str = "Validation failed. Please check your input.",
) -> Response:
    """
    Create a standardized validation error response.

    Args:
        field_errors: Dictionary mapping field names to error messages
        message: Validation error message

    Returns:
        DRF Response object with 400 status

    Example:
        return validation_error_response({
            "email": ["This field is required."],
            "password": ["Must be at least 6 characters."]
        })
    """
    return error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        details=field_errors,
        status_code=http_status.HTTP_400_BAD_REQUEST,
    )
