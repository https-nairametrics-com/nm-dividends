# Architecture Overview

System architecture and design documentation for NM Dividends Backend.

---

## High-Level Architecture

```
                    ┌─────────────────────────────────────────┐
                    │           Client Layer                  │
                    │  ┌─────────┐      ┌──────────────┐     │
                    │  │ Web App │      │ Mobile Apps  │     │
                    │  └────┬────┘      └──────┬───────┘     │
                    └───────┼──────────────────┼─────────────┘
                            │                  │
                            └──────────┬───────┘
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │            API Layer                    │
                    │  ┌─────────────────┐  ┌────────────┐   │
                    │  │ Django REST FW  │  │ JWT Auth   │   │
                    │  └────────┬────────┘  └─────┬──────┘   │
                    └───────────┼─────────────────┼──────────┘
                                │                 │
              ┌─────────────────┘                 └──────────────────┐
              ▼                                                      ▼
┌─────────────────────────────┐                         ┌─────────────────────────────┐
│        Active Apps          │                         │       Legacy Apps           │
│  ┌──────────┬──────────┐    │                         │  ┌──────────────────────┐   │
│  │   auth   │ results  │    │                         │  │ article              │   │
│  └──────────┴──────────┘    │                         │  │ investment           │   │
│                             │                         │  │ investor             │   │
└─────────────────────────────┘                         │  │ expenses             │   │
                                                        │  │ comment              │   │
                                                        │  │ contact              │   │
                                                        │  │ social_auth          │   │
                                                        └─────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│           Data Layer                    │
│  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │ Media Storage│     │
│  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────┘
```

---

## System Components

| Component | Purpose | Status |
|-----------|---------|--------|
| `authentication` | User management, JWT auth, email verification | **Active** |
| `results` | NM Data CSV uploads and results tracking | **Active** |
| `article` | Legacy article management | Deprecated |
| `investment` | Investment portfolios | Deprecated |
| `investor` | Investor profiles | Deprecated |
| `expenses` | Expense tracking | Deprecated |
| `comment` | Comment system | Deprecated |
| `contact` | Contact forms | Deprecated |
| `social_auth` | OAuth providers | Deprecated |

---

## Directory Structure

```
nm-dividends-backend/
├── authentication/          # User authentication and management (ACTIVE)
│   ├── models.py           # User, Referrals models
│   ├── views.py            # Auth views (register, login, verify, etc.)
│   ├── serializers.py      # User serializers
│   ├── urls.py             # Auth routes
│   └── tests/              # Authentication tests
├── results/                # NM Data CSV uploads (ACTIVE)
│   ├── models.py           # NMData model
│   ├── views.py            # CSV upload, list, update views
│   ├── serializers.py      # NMData serializers
│   └── urls.py             # Results API routes
├── article/                # Legacy (deprecated)
├── investment/             # Legacy (deprecated)
├── investor/               # Legacy (deprecated)
├── expenses/               # Legacy (deprecated)
├── comment/                # Legacy (deprecated)
├── contact/                # Legacy (deprecated)
├── social_auth/            # Legacy (deprecated)
├── dividends/              # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py/asgi.py     # WSGI/ASGI entry points
├── docs/                   # Documentation
├── media/                  # Uploaded files
├── static/                 # Static files
├── manage.py               # Django management
├── requirements.txt        # Python dependencies
└── .env-example            # Environment variables template
```

---

## Technology Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 3.2.16 | Web framework |
| djangorestframework | 3.13.1 | REST API framework |
| djangorestframework-simplejwt | 5.2.2 | JWT authentication |
| django-cors-headers | 3.13.0 | CORS handling |
| django-filter | 22.1 | Query filtering |
| drf-yasg | 1.20.0 | OpenAPI/Swagger docs |
| dj-database-url | 1.0.0 | Database configuration |
| psycopg2 | 2.9.5+ | PostgreSQL adapter |
| python-dotenv | 0.21.0 | Environment variables |
| gunicorn | 20.1.0 | WSGI server |
| whitenoise | 6.2.0+ | Static files |

### Additional Libraries

| Package | Purpose |
|---------|---------|
| Pillow | Image processing |
| pandas | Data manipulation |
| reportlab/fpdf | PDF generation |
| chardet | Character encoding detection |

---

## Request Flow

1. **Client** makes HTTP request
2. **CORS Middleware** validates origin
3. **JWT Authentication** validates token (if required)
4. **Django Router** routes to appropriate view
5. **View/ViewSet** processes request
6. **Serializer** validates data
7. **Model** interacts with database
8. **Response** returned with standardized format

---

*Last Updated: 2026-04-03*
