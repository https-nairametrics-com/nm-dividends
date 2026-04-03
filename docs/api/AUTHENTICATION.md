# Authentication API

Complete reference for authentication endpoints.

---

## Overview

The authentication system uses JWT (JSON Web Tokens) via Django REST Framework SimpleJWT. Two token types are issued:
- **Access Token**: Short-lived (configurable), used for API authentication
- **Refresh Token**: Longer-lived, used to obtain new access tokens

---

## JWT Token Endpoints

### Obtain Token Pair

Obtain both access and refresh tokens.

```bash
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

### Refresh Token

Obtain a new access token using a refresh token.

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Verify Token

Verify if a token is valid.

```bash
POST /api/token/verify/
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200 OK):**
```json
{}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Auth Endpoints (`/auth/`)

### Register User

Register a new user account. Sends verification email.

```bash
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "firstname": "John",
  "lastname": "Doe"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "username": "JohnDoe12345",
  "referral_code": "ABC123XYZ",
  "is_verified": false,
  "is_approved": true,
  "is_active": true,
  "is_staff": false,
  "created_at": "2026-04-03T10:00:00Z",
  "updated_at": "2026-04-03T10:00:00Z"
}
```

**Error Response (400 Bad Request) - Validation Errors:**
```json
{
  "email": ["user with this email already exists."],
  "password": ["This field is required."]
}
```

**Error Response (400 Bad Request) - Duplicate Email:**
```json
{
  "email": ["user with this email already exists."]
}
```

### Login

Login with email and password. Returns user data and tokens.

```bash
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "id": 1,
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "username": "JohnDoe12345",
  "is_verified": true,
  "is_approved": true,
  "is_active": true,
  "is_staff": false,
  "created_at": "2026-04-03T10:00:00Z",
  "updated_at": "2026-04-03T10:00:00Z"
}
```

**Error Response (401 Unauthorized) - Invalid Credentials:**
```json
{
  "detail": "Invalid credentials, try again"
}
```

**Note:** The login endpoint validates email/password and returns SimpleJWT tokens along with user data.

### Verify Email

Verify user email using token from verification email.

```bash
GET /auth/email-verify/?token=<jwt_token>
```

**Success Response (200 OK):**
```json
{
  "email": "Successfully activated"
}
```

**Error Response (400 Bad Request) - Expired Token:**
```json
{
  "error": "Activation Expired"
}
```

**Error Response (400 Bad Request) - Invalid Token:**
```json
{
  "error": "Invalid token"
}
```

### Request Password Reset

Request a password reset email.

```bash
POST /auth/request-reset-email/
Content-Type: application/json

{
  "email": "user@example.com",
  "callbackUrl": "https://example.com/reset",
  "redirect_url": "https://example.com/redirect"
}
```

**Success Response (200 OK):**
```json
{
  "success": "We have sent you a link to reset your password"
}
```

**Note:** Always returns 200 OK even if email doesn't exist (security). Email is sent using Django's send_mail.

### Password Reset Check

Check if password reset token is valid. Redirects to frontend.

```bash
GET /auth/password-reset/<uidb64>/<token>/?redirect_url=<frontend_url>
```

**Success (302 Redirect):**
```
Location: https://frontend.com/?token_valid=True&message=Credentials Valid&uidb64=<uidb64>&token=<token>
```

**Error (302 Redirect):**
```
Location: https://frontend.com/?token_valid=False
```

**Error Response (400 Bad Request) - Invalid Token:**
```json
{
  "error": "Token is not valid, please request a new one"
}
```

### Set New Password

Complete password reset with new password.

```bash
PATCH /auth/password-reset-complete
Content-Type: application/json

{
  "password": "NewSecurePassword123!",
  "token": "<token_from_redirect>",
  "uidb64": "<uidb64_from_redirect>"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset success"
}
```

**Error Response (400 Bad Request):**
```json
{
  "password": ["This field is required."],
  "token": ["This field is required."],
  "uidb64": ["This field is required."]
}
```

### Logout

Logout user by blacklisting the refresh token.

```bash
POST /auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (204 No Content):**
*(Empty response body)*

**Error Response (400 Bad Request) - Invalid Token:**
```json
{
  "refresh": ["Token is invalid or expired"]
}
```

**Error Response (401 Unauthorized) - No Token:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Load User

Get current authenticated user data.

```bash
GET /auth/loaduser/
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "username": "JohnDoe12345",
    "referral_code": "ABC123XYZ",
    "is_verified": true,
    "is_approved": true,
    "is_active": true,
    "is_staff": false,
    "created_at": "2026-04-03T10:00:00Z",
    "updated_at": "2026-04-03T10:00:00Z"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Something went wrong when trying to load user"
}
```

### Get Referral Info

Get user info by referral code.

```bash
GET /auth/invite/?user=<referral_code>
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "referral_code": "ABC123XYZ",
    "is_approved": true
  }
}
```

**Error Response (400 Bad Request) - Not Found:**
```json
{
  "status": "error",
  "error": "Object with referral code does not exists"
}
```

**Error Response (400 Bad Request) - Not Approved:**
```json
{
  "status": "error",
  "error": "Object with referral code does not exists"
}
```

---

## Admin Endpoints

These endpoints require admin (`is_staff=True`) authentication.

### List Users

List all users with filtering and pagination.

```bash
GET /auth/list-users/?firstname=John&search=john&ordering=-created_at
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `firstname` - Filter by first name
- `lastname` - Filter by last name
- `phone` - Filter by phone
- `email` - Filter by email
- `referral_code` - Filter by referral code
- `search` - Search across multiple fields
- `ordering` - Sort by field (prefix with `-` for descending)

**Success Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/auth/list-users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "user@example.com",
      "firstname": "John",
      "lastname": "Doe",
      "is_verified": true,
      "is_approved": true,
      "created_at": "2026-04-03T10:00:00Z"
    }
  ]
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Get/Update/Delete User

Manage specific user.

```bash
# Get user
GET /auth/user/1
Authorization: Bearer <admin_token>

# Update user
PUT /auth/user/1
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "firstname": "Jane",
  "lastname": "Doe"
}

# Delete user
DELETE /auth/user/1
Authorization: Bearer <admin_token>
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

### Approve User

Approve or unapprove a user.

```bash
PATCH /auth/approve/1
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "is_approved": true
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_approved": true
}
```

### Verify User

Manually verify or unverify a user.

```bash
PATCH /auth/verify/1
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "is_verified": true
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_verified": true
}
```

---

## Legacy/Deprecated Endpoints

These endpoints are part of the legacy investment system and are deprecated:

| Endpoint | Status | Notes |
|----------|--------|-------|
| `POST /auth/sign-in/` | Deprecated | Alternative login with cookie-based JWT |
| `POST /auth/register/issuer/` | Deprecated | Register issuer with profile |
| `POST /auth/register/referral/` | Deprecated | Register with referral code |
| `POST /auth/initial-interest/` | Deprecated | Create investment interest |
| `PUT /auth/initial-interest/update/<id>` | Deprecated | Update investment interest |
| `GET /auth/export/users/` | Deprecated | Export users to CSV |
| `GET /auth/export/users/pdf/` | Deprecated | Export users to PDF |

**Do not use these endpoints for new development.**

---

## Error Response Reference

### Common HTTP Status Codes

| Code | Meaning | When Returned |
|------|---------|---------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (register) |
| 204 | No Content | Successful DELETE, Logout |
| 400 | Bad Request | Validation error, invalid token |
| 401 | Unauthorized | Invalid credentials, expired token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | User/resource doesn't exist |
| 500 | Server Error | Unexpected server error |

### JWT Token Errors

| Error | Message | Cause |
|-------|---------|-------|
| `token_not_valid` | "Token is invalid or expired" | Invalid or expired JWT |
| `token_blacklisted` | "Token has been blacklisted" | Logged out token |
| `no_active_account` | "No active account found..." | Wrong email/password |

---

## Authentication Flow

### Registration Flow

```
1. POST /auth/register/ → 201 + user data
2. User receives email with verification link
3. GET /auth/email-verify/?token=... → 200
4. User can now login
```

### Login Flow

```
1. POST /auth/login/ → 200 + tokens + user data
2. Use access token in Authorization header
3. When access expires, POST /api/token/refresh/
4. On logout, POST /auth/logout/ with refresh token
```

### Password Reset Flow

```
1. POST /auth/request-reset-email/ → 200
2. User receives email with reset link
3. GET /auth/password-reset/<uidb64>/<token>/ → Redirects to frontend
4. Frontend extracts token and uidb64 from URL
5. PATCH /auth/password-reset-complete → 200
```

---

*Last Updated: 2026-04-03*
