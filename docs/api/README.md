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

| Endpoint | App | Description | Auth Required |
|----------|-----|-------------|---------------|
| `/auth/register/` | authentication | User registration | No |
| `/auth/login/` | authentication | User login | No |
| `/api/token/` | authentication | Obtain JWT tokens | No |
| `/api/token/refresh/` | authentication | Refresh access token | No |
| `/auth/loaduser/` | authentication | Current user info | Yes |
| `/article/posts/` | article | List articles | No |
| `/article/posts/<slug>/` | article | Get single article | No |
| `/results/` | results | List NMData uploads | No |
| `/results/upload/` | results | Upload CSV file | Yes (Admin) |

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
