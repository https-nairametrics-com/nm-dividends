"""
Tests for standardized response utilities and exception handler.
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
    PermissionDenied,
    NotFound,
)

from authentication.responses import (
    api_response,
    success_response,
    error_response,
    created_response,
    deleted_response,
    validation_error_response,
    paginated_response,
)
from authentication.error_codes import ErrorCode
from authentication.exceptions import custom_exception_handler, _map_exception_to_error_code


class TestApiResponse(TestCase):
    """Tests for the api_response utility function."""

    def test_api_response_success(self):
        """Test successful api_response with all fields."""
        response = api_response(
            success=True,
            message="Test message",
            data={"key": "value"},
            meta={"page": 1},
            status_code=status.HTTP_200_OK,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Test message")
        self.assertEqual(response.data["data"], {"key": "value"})
        self.assertEqual(response.data["meta"], {"page": 1})

    def test_api_response_error(self):
        """Test error api_response."""
        response = api_response(
            success=False,
            message="Error occurred",
            error={"code": "TEST_ERROR", "details": "Test error details"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["message"], "Error occurred")
        self.assertEqual(response.data["error"]["code"], "TEST_ERROR")

    def test_api_response_minimal(self):
        """Test api_response with minimal fields."""
        response = api_response()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "")
        self.assertNotIn("data", response.data)
        self.assertNotIn("error", response.data)


class TestSuccessResponse(TestCase):
    """Tests for success_response utility."""

    def test_success_response_basic(self):
        """Test basic success response."""
        response = success_response(
            data={"id": 1},
            message="Resource created"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Resource created")
        self.assertEqual(response.data["data"], {"id": 1})

    def test_success_response_with_meta(self):
        """Test success response with pagination metadata."""
        response = success_response(
            data=[{"id": 1}, {"id": 2}],
            message="List retrieved",
            meta={"current_page": 1, "per_page": 10, "total": 2}
        )

        self.assertEqual(response.data["meta"]["current_page"], 1)
        self.assertEqual(response.data["meta"]["total"], 2)


class TestErrorResponse(TestCase):
    """Tests for error_response utility."""

    def test_error_response_with_code(self):
        """Test error response with error code."""
        response = error_response(
            error_code=ErrorCode.NOT_FOUND,
            details="Resource not found"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["error"]["code"], "NOT_FOUND")
        self.assertEqual(response.data["error"]["details"], "Resource not found")

    def test_error_response_default_message(self):
        """Test error response uses default message from error code."""
        response = error_response(error_code=ErrorCode.AUTHENTICATION_FAILED)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)
        self.assertIn("Authentication failed", response.data["message"])

    def test_error_response_validation(self):
        """Test validation error response."""
        field_errors = {"email": ["This field is required"]}
        response = validation_error_response(field_errors)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["code"], "VALIDATION_ERROR")
        self.assertEqual(response.data["error"]["details"], field_errors)


class TestCreatedResponse(TestCase):
    """Tests for created_response utility."""

    def test_created_response(self):
        """Test created response returns 201 status."""
        response = created_response(
            data={"id": 1, "name": "Test"},
            message="Resource created successfully"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["data"]["id"], 1)


class TestDeletedResponse(TestCase):
    """Tests for deleted_response utility."""

    def test_deleted_response(self):
        """Test deleted response."""
        response = deleted_response(message="User deleted")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "User deleted")


class TestPaginatedResponse(TestCase):
    """Tests for paginated_response utility."""

    def test_paginated_response(self):
        """Test paginated response with metadata."""
        data = [{"id": 1}, {"id": 2}]
        response = paginated_response(
            data=data,
            page=1,
            per_page=10,
            total=25,
            message="Resources retrieved"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"], data)
        self.assertEqual(response.data["meta"]["current_page"], 1)
        self.assertEqual(response.data["meta"]["per_page"], 10)
        self.assertEqual(response.data["meta"]["total"], 25)
        self.assertEqual(response.data["meta"]["total_pages"], 3)


class TestExceptionHandler(TestCase):
    """Tests for custom_exception_handler."""

    def test_map_authentication_failed(self):
        """Test mapping of AuthenticationFailed exception."""
        exc = AuthenticationFailed("Invalid credentials")
        class MockResponse:
            status_code = 401
            data = {"detail": "Invalid credentials"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.AUTHENTICATION_FAILED)

    def test_map_not_authenticated(self):
        """Test mapping of NotAuthenticated exception."""
        exc = NotAuthenticated("Authentication required")
        class MockResponse:
            status_code = 401
            data = {"detail": "Authentication required"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.NOT_AUTHENTICATED)

    def test_map_validation_error(self):
        """Test mapping of ValidationError exception."""
        exc = ValidationError({"email": ["This field is required"]})
        class MockResponse:
            status_code = 400
            data = {"email": ["This field is required"]}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.VALIDATION_ERROR)
        self.assertEqual(details, {"email": ["This field is required"]})

    def test_map_permission_denied(self):
        """Test mapping of PermissionDenied exception."""
        exc = PermissionDenied("Permission denied")
        class MockResponse:
            status_code = 403
            data = {"detail": "Permission denied"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.PERMISSION_DENIED)

    def test_map_not_found(self):
        """Test mapping of NotFound exception."""
        exc = NotFound("Resource not found")
        class MockResponse:
            status_code = 404
            data = {"detail": "Resource not found"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.NOT_FOUND)

    def test_map_expired_token(self):
        """Test mapping of expired token error."""
        exc = AuthenticationFailed({"detail": "Token has expired"})
        class MockResponse:
            status_code = 401
            data = {"detail": "Token has expired"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.EXPIRED_TOKEN)

    def test_map_invalid_token(self):
        """Test mapping of invalid token error."""
        exc = AuthenticationFailed({"detail": "Invalid token"})
        class MockResponse:
            status_code = 401
            data = {"detail": "Invalid token"}

        error_code, details = _map_exception_to_error_code(exc, MockResponse())

        self.assertEqual(error_code, ErrorCode.INVALID_TOKEN)


class TestErrorCodes(TestCase):
    """Tests for ErrorCode enum and error info."""

    def test_all_error_codes_have_status(self):
        """Test that all error codes have HTTP status mappings."""
        from authentication.error_codes import ERROR_HTTP_STATUS

        for code in ErrorCode:
            self.assertIn(code, ERROR_HTTP_STATUS)

    def test_error_code_values(self):
        """Test error code string values."""
        self.assertEqual(ErrorCode.AUTHENTICATION_FAILED.value, "AUTHENTICATION_FAILED")
        self.assertEqual(ErrorCode.NOT_FOUND.value, "NOT_FOUND")
        self.assertEqual(ErrorCode.VALIDATION_ERROR.value, "VALIDATION_ERROR")
