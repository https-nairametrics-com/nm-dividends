"""
Error codes for standardized API error handling.

This module defines all error codes used across the API for consistent
error identification and handling on the frontend.
"""

from enum import Enum


class ErrorCode(Enum):
    """Base error codes for the API."""

    # Authentication Errors (1xx)
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    USERNAME_EXISTS = "USERNAME_EXISTS"
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_BLACKLISTED = "TOKEN_BLACKLISTED"

    # Referral Errors (2xx)
    REFERRAL_CODE_INVALID = "REFERRAL_CODE_INVALID"
    REFERRAL_CODE_LIMIT = "REFERRAL_CODE_LIMIT"
    REFERRAL_SELF = "REFERRAL_SELF"

    # Authorization Errors (3xx)
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    ADMIN_REQUIRED = "ADMIN_REQUIRED"
    EDITOR_REQUIRED = "EDITOR_REQUIRED"
    OWNER_REQUIRED = "OWNER_REQUIRED"

    # Resource Errors (4xx)
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_STATUS = "INVALID_STATUS"
    SLUG_EXISTS = "SLUG_EXISTS"

    # File Upload Errors (5xx)
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"
    NO_FILE_PROVIDED = "NO_FILE_PROVIDED"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"

    # Server Errors (9xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    EMAIL_SEND_FAILED = "EMAIL_SEND_FAILED"


# Error code to HTTP status mapping
ERROR_HTTP_STATUS = {
    # Authentication
    ErrorCode.AUTHENTICATION_FAILED: 401,
    ErrorCode.EMAIL_EXISTS: 409,
    ErrorCode.USERNAME_EXISTS: 409,
    ErrorCode.INVALID_TOKEN: 401,
    ErrorCode.EXPIRED_TOKEN: 401,
    ErrorCode.EMAIL_NOT_VERIFIED: 403,
    ErrorCode.ACCOUNT_DISABLED: 403,
    ErrorCode.INVALID_CREDENTIALS: 401,
    ErrorCode.TOKEN_BLACKLISTED: 401,
    # Referral
    ErrorCode.REFERRAL_CODE_INVALID: 400,
    ErrorCode.REFERRAL_CODE_LIMIT: 400,
    ErrorCode.REFERRAL_SELF: 400,
    # Authorization
    ErrorCode.PERMISSION_DENIED: 403,
    ErrorCode.NOT_AUTHENTICATED: 401,
    ErrorCode.ADMIN_REQUIRED: 403,
    ErrorCode.EDITOR_REQUIRED: 403,
    ErrorCode.OWNER_REQUIRED: 403,
    # Resource
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.ALREADY_EXISTS: 409,
    ErrorCode.VALIDATION_ERROR: 400,
    ErrorCode.INVALID_STATUS: 400,
    ErrorCode.SLUG_EXISTS: 409,
    # File Upload
    ErrorCode.FILE_TOO_LARGE: 413,
    ErrorCode.INVALID_FILE_TYPE: 415,
    ErrorCode.FILE_UPLOAD_FAILED: 500,
    ErrorCode.NO_FILE_PROVIDED: 400,
    ErrorCode.FILE_NOT_FOUND: 404,
    # Server
    ErrorCode.INTERNAL_ERROR: 500,
    ErrorCode.DATABASE_ERROR: 500,
    ErrorCode.SERVICE_UNAVAILABLE: 503,
    ErrorCode.EMAIL_SEND_FAILED: 500,
}


# User-friendly error messages and help text
ERROR_MESSAGES = {
    # Authentication
    ErrorCode.AUTHENTICATION_FAILED: {
        "message": "Authentication failed. Please check your credentials.",
        "help": "Please verify your email and password, or reset your password if you've forgotten it.",
    },
    ErrorCode.EMAIL_EXISTS: {
        "message": "This email address is already registered.",
        "help": "Please use a different email address or try logging in if you already have an account.",
    },
    ErrorCode.USERNAME_EXISTS: {
        "message": "This username is already taken.",
        "help": "Please choose a different username.",
    },
    ErrorCode.INVALID_TOKEN: {
        "message": "Invalid authentication token.",
        "help": "Your session may have expired. Please log in again.",
    },
    ErrorCode.EXPIRED_TOKEN: {
        "message": "Your session has expired.",
        "help": "Please log in again to continue.",
    },
    ErrorCode.EMAIL_NOT_VERIFIED: {
        "message": "Please verify your email address.",
        "help": "Check your email for a verification link, or request a new verification email.",
    },
    ErrorCode.ACCOUNT_DISABLED: {
        "message": "Your account has been disabled.",
        "help": "Please contact support for assistance.",
    },
    ErrorCode.INVALID_CREDENTIALS: {
        "message": "Invalid email or password.",
        "help": "Please check your credentials and try again.",
    },
    # Referral
    ErrorCode.REFERRAL_CODE_INVALID: {
        "message": "Invalid referral code.",
        "help": "Please check the referral code and try again.",
    },
    ErrorCode.REFERRAL_CODE_LIMIT: {
        "message": "This referral code has reached its usage limit.",
        "help": "Please try a different referral code.",
    },
    # Authorization
    ErrorCode.PERMISSION_DENIED: {
        "message": "You don't have permission to perform this action.",
        "help": "Please contact your administrator if you need access to this feature.",
    },
    ErrorCode.NOT_AUTHENTICATED: {
        "message": "Authentication required.",
        "help": "Please log in to access this resource.",
    },
    ErrorCode.ADMIN_REQUIRED: {
        "message": "Admin access required.",
        "help": "This feature is restricted to administrators only.",
    },
    ErrorCode.EDITOR_REQUIRED: {
        "message": "Editor access required.",
        "help": "This feature is restricted to editors and administrators.",
    },
    # Resource
    ErrorCode.NOT_FOUND: {
        "message": "The requested resource was not found.",
        "help": "Please check the identifier and try again.",
    },
    ErrorCode.ALREADY_EXISTS: {
        "message": "This resource already exists.",
        "help": "Please use a different identifier or update the existing resource.",
    },
    ErrorCode.VALIDATION_ERROR: {
        "message": "Validation failed. Please check your input.",
        "help": "Please ensure all required fields are filled correctly.",
    },
    # File Upload
    ErrorCode.FILE_TOO_LARGE: {
        "message": "The uploaded file is too large.",
        "help": "Please upload a file smaller than 5MB.",
    },
    ErrorCode.INVALID_FILE_TYPE: {
        "message": "Unsupported file format.",
        "help": "Please upload a JPEG, PNG, GIF, or WebP image.",
    },
    ErrorCode.NO_FILE_PROVIDED: {
        "message": "No file was provided.",
        "help": "Please select a file to upload.",
    },
    # Server
    ErrorCode.INTERNAL_ERROR: {
        "message": "An unexpected error occurred.",
        "help": "Please try again later. If the problem persists, contact support.",
    },
    ErrorCode.SERVICE_UNAVAILABLE: {
        "message": "Service temporarily unavailable.",
        "help": "Please try again in a few moments.",
    },
}


def get_error_info(error_code: ErrorCode) -> dict:
    """
    Get user-friendly error information for an error code.

    Args:
        error_code: The ErrorCode enum value

    Returns:
        Dictionary with message, help, and HTTP status
    """
    default_info = {
        "message": "An error occurred.",
        "help": "Please try again or contact support if the problem persists.",
    }

    info = ERROR_MESSAGES.get(error_code, default_info)

    return {
        "code": error_code.value,
        "message": info["message"],
        "help": info["help"],
        "status": ERROR_HTTP_STATUS.get(error_code, 500),
    }
