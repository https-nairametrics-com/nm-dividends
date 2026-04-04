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

### Active Apps (API Available)

```
authentication/  # User management, JWT auth
article/         # Content management (articles, news, disclosures)
results/         # NM Data CSV uploads and results tracking
```

### In Development

```
resources/       # Content management (next-gen, models ready, API pending)
```

### Legacy/Disabled Apps

```
income/          # Income tracking (disabled, not in INSTALLED_APPS)
investor/        # Legacy (deprecated)
investment/      # Legacy (deprecated)
comment/         # Legacy (deprecated)
contact/         # Legacy (deprecated)
social_auth/     # Legacy (deprecated)
```

---

*See [Docs README](../README.md) for full documentation index*
