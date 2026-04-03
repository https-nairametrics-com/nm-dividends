# API Documentation

Complete reference for the NM Dividends Backend API.

---

## Interactive Documentation

- **Swagger UI:** http://localhost:8000/
- **ReDoc:** http://localhost:8000/redoc/

## Documents

| Document | Description |
|----------|-------------|
| [AUTHENTICATION.md](./AUTHENTICATION.md) | Authentication API (JWT, login, register, password reset) |
| [RESULTS.md](./RESULTS.md) | Results/NMData CSV upload API |
| [ERROR_CODES.md](./ERROR_CODES.md) | Error handling reference |

## API Overview

### Base URL
```
http://localhost:8000/
```

### Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Main Endpoints

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `/auth/register/` | User registration | No |
| `/auth/login/` | User login | No |
| `/api/token/` | Obtain JWT tokens | No |
| `/api/token/refresh/` | Refresh access token | No |
| `/auth/loaduser/` | Current user info | Yes |
| `/results/` | List NMData uploads | No |
| `/results/upload/` | Upload CSV file | Yes (Admin) |

### Response Formats

We are standardizing all responses to use this format:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "meta": { ... }  // For list endpoints
}
```

See [ERROR_CODES.md](./ERROR_CODES.md) for error response formats.

---

*See [Docs README](../README.md) for full documentation index*
