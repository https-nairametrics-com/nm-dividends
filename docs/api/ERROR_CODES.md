# NM Dividends Backend - API Error Reference

This document provides a comprehensive reference for all API error responses.

---

## HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or token invalid |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists (duplicate) |
| 413 | Payload Too Large | File exceeds size limit |
| 415 | Unsupported Media Type | Invalid file type |
| 422 | Unprocessable Entity | Validation error (semantic) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Authentication Errors

### Registration Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `EMAIL_EXISTS` | 400 | "User with this email already exists." | Duplicate email |
| `USERNAME_EXISTS` | 400 | "User with this username already exists." | Duplicate username |
| `INVALID_EMAIL` | 400 | "Enter a valid email address." | Malformed email |
| `WEAK_PASSWORD` | 400 | "Password too weak." | Password validation failed |
| `PASSWORD_MISMATCH` | 400 | "Passwords do not match." | Confirm password mismatch |

**Example Response:**
```json
{
  "status": "error",
  "errors": {
    "email": ["User with this email already exists."],
    "password": ["This password is too short. It must contain at least 8 characters."]
  }
}
```

### Login Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `INVALID_CREDENTIALS` | 401 | "Invalid credentials, try again" | Wrong email/password |
| `EMAIL_NOT_VERIFIED` | 403 | "Email is not verified" | User not verified |
| `ACCOUNT_DISABLED` | 403 | "Account is disabled" | User is_active=False |
| `ACCOUNT_NOT_APPROVED` | 403 | "Account pending approval" | User is_approved=False |

**Example Response:**
```json
{
  "status": "error",
  "error": "Invalid credentials, try again"
}
```

### Token Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `TOKEN_INVALID` | 401 | "Token is invalid or expired" | Invalid JWT token |
| `TOKEN_EXPIRED` | 401 | "Token has expired" | Access token expired |
| `REFRESH_INVALID` | 401 | "Refresh token is invalid" | Invalid refresh token |
| `REFRESH_EXPIRED` | 401 | "Refresh token has expired" | Refresh token expired |
| `TOKEN_BLACKLISTED` | 401 | "Token has been blacklisted" | Logged out token |

**Example Response:**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Password Reset Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `RESET_INVALID_TOKEN` | 400 | "Invalid token" | Bad reset token |
| `RESET_EXPIRED` | 400 | "Reset link expired" | Token expired |
| `RESET_USER_NOT_FOUND` | 400 | "User not found" | UIDB64 invalid |
| `PASSWORD_SAME_AS_OLD` | 400 | "New password cannot be same as old" | No change password |

### Permission Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `AUTH_REQUIRED` | 401 | "Authentication credentials were not provided." | Missing token |
| `NOT_ADMIN_EDITOR` | 403 | "You do not have permission to perform this action." | User not staff |
| `NOT_OWNER` | 403 | "You can only modify your own data." | Non-owner edit |

**Example Response:**
```json
{
  "success": false,
  "message": "Authentication required",
  "errors": {
    "detail": "Authentication credentials were not provided."
  }
}
```

---

## Media Upload Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `FILE_REQUIRED` | 400 | "No file provided." | Missing file field |
| `FILE_TOO_LARGE` | 413 | "File size exceeds 5MB limit." | File > 5MB |
| `INVALID_FILE_TYPE` | 415 | "Invalid file type. Allowed: JPEG, PNG, GIF, WebP." | Wrong MIME type |
| `UPLOAD_FAILED` | 500 | "Failed to save file." | Server error |

**Example Response:**
```json
{
  "success": false,
  "message": "File size exceeds 5MB limit.",
  "errors": {
    "file": ["Maximum file size is 5MB."]
  }
}
```

### Allowed File Types

| Extension | MIME Type |
|-----------|-----------|
| .jpg, .jpeg | image/jpeg |
| .png | image/png |
| .gif | image/gif |
| .webp | image/webp |

---

## Email Errors

| Error Code | HTTP Status | Message | Cause |
|------------|-------------|---------|-------|
| `EMAIL_SEND_FAILED` | 500 | "Failed to send email." | SMTP error |
| `EMAIL_NOT_FOUND` | 404 | "User with this email does not exist." | Wrong email for reset |

---

## Validation Error Formats

### Target Standard Format

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "field_name": ["Error message 1", "Error message 2"]
  }
}
```

### Legacy Format (authentication app)

```json
{
  "status": "error",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

### DRF Default Format (article app)

```json
{
  "field_name": ["Error message"]
}
```

---

## Error Handling Best Practices

### For Frontend Developers

1. **Always check status codes first**
   ```javascript
   if (response.status === 401) {
     // Redirect to login
   }
   ```

2. **Handle validation errors by field**
   ```javascript
   const errors = response.data.errors;
   if (errors.email) {
     showEmailError(errors.email[0]);
   }
   ```

3. **Display user-friendly messages**
   ```javascript
   const errorMessages = {
     'EMAIL_EXISTS': 'An account with this email already exists.',
     'INVALID_CREDENTIALS': 'Incorrect email or password.',
     'TOKEN_EXPIRED': 'Your session has expired. Please log in again.'
   };
   ```

4. **Handle network errors**
   ```javascript
   try {
     const response = await api.get('/results/');
   } catch (error) {
     if (!error.response) {
       // Network error - no connection
       showError('Please check your internet connection.');
     }
   }
   ```

### For Backend Developers

1. **Use consistent error formats** (migrate to standard format)
2. **Include helpful error messages**
3. **Don't expose sensitive information** in errors
4. **Log errors appropriately** for debugging

---

## Migration to Standardized Errors (Issue #9)

We are migrating all endpoints to use a consistent error format:

```json
{
  "success": false,
  "message": "Human-readable description",
  "errors": {
    "field": ["Specific error"]
  }
}
```

### Progress (Active Apps Only)

| App | Current Format | Target Format | Status |
|-----|---------------|---------------|--------|

| authentication | Legacy | Standard | 🔄 In Progress |
| results | Custom | Standard | ⏳ Pending |

---

*Last Updated: 2026-04-03*
