# Architecture Documentation

System design and architecture documentation.

---

## Documents

| Document | Description |
|----------|-------------|
| [OVERVIEW.md](./OVERVIEW.md) | High-level system architecture |
| [DATA_MODELS.md](./DATA_MODELS.md) | Database schema and models |
| [AUTHENTICATION.md](./AUTHENTICATION.md) | Auth flow and permissions |

---

## System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  Django API │────▶│  PostgreSQL │
│  (React)    │     │   (DRF)     │     │   (Data)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Components

| Component | Purpose | Tech |
|-----------|---------|------|
| Django | Web framework | Python 3.9+ |
| DRF | REST API | Django REST Framework |
| JWT | Authentication | SimpleJWT |
| PostgreSQL | Database | psycopg2 |
| Whitenoise | Static files | Whitenoise |
| Gunicorn | WSGI server | Gunicorn |

## Apps Structure

### Active Apps

```
authentication/  # User management, JWT auth
results/         # NM Data CSV uploads and results tracking
```

### Legacy Apps (Deprecated)

```
article/         # Legacy - deprecated
investment/      # Legacy - deprecated
investor/        # Legacy - deprecated
expenses/        # Legacy - deprecated
comment/         # Legacy - deprecated
contact/         # Legacy - deprecated
social_auth/     # Legacy - deprecated
```

> **Note:** Do not build new features on legacy apps.

---

*See [Docs README](../README.md) for full documentation index*
